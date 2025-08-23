# cloud_entry.py
import os
import importlib
import json
import boto3
from botocore.client import Config

# Import your original app module (the file is app.py)
m = importlib.import_module("app")

# We’ll reuse jsonify from your module (same Flask app context)
jsonify = m.jsonify

# S3 setup
S3_BUCKET = os.environ.get("ARTIFACT_BUCKET", "")
if not S3_BUCKET:
    raise RuntimeError("Set ARTIFACT_BUCKET env var to your S3 bucket name")

_s3 = boto3.client("s3", config=Config(signature_version="s3v4"))

def _upload_and_presign(local_path: str, key: str, expires: int = 3600) -> str:
    _s3.upload_file(local_path, S3_BUCKET, key)
    return _s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": S3_BUCKET, "Key": key},
        ExpiresIn=expires,
    )

def _key_for(local_path: str) -> str:
    # Put your own keying scheme here if you want per-user, timestamps, etc.
    # Default: mirror filename under "output/"
    base = os.path.basename(local_path)
    return f"output/{base}"

def cloud_send_file(local_path, *args, **kwargs):
    """
    Drop-in replacement for flask.send_file that:
      - ensures the file exists (wherever your code wrote it),
      - uploads it to S3,
      - returns a JSON with a presigned URL.
    We ignore flask.send_file’s other kwargs by design in cloud mode.
    """
    if not os.path.isabs(local_path):
        # Respect current working directory; Lambda often uses /var/task
        local_path = os.path.abspath(local_path)

    if not os.path.exists(local_path):
        return jsonify({"error": f"File not found: {local_path}"}), 500

    key = _key_for(local_path)
    url = _upload_and_presign(local_path, key)
    return jsonify({"url": url}), 200

# ---- MONKEY-PATCH: replace the name `send_file` in the app module ----
m.send_file = cloud_send_file

# Expose the same Flask app object for your server (gunicorn/Lambda)
app = m.app
