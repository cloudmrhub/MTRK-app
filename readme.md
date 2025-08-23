
Here’s a **mini-README** you can drop in your repo (e.g. `README-cloud.md`) to explain the **cloud release of MTRK** from an IT/DevOps point of view:

---

# MTRK – Cloud Release (Serverless)

This release packages **MTRK** into a **serverless backend** that runs on **AWS Lambda behind API Gateway**, with outputs stored in **S3**. The goal is to make MTRK usable as a scalable web service without modifying the original codebase.

---

## 🎯 Key Ideas

* **Preserve the core MTRK repo**
  We don’t touch the original `app.py` or `mtrk_designer_api`.
  Instead, we introduced a lightweight shim called **`cloud_entry.py`**.

* **cloud\_entry.py**

  * Imports the existing `app` (Flask) from `app.py`.
  * Monkey-patches `send_file(...)` so instead of sending files directly, it:

    1. Writes files into `/tmp`
    2. Uploads them to **S3** (bucket defined by `ARTIFACT_BUCKET`)
    3. Returns a **presigned URL** to the client.
  * Exposes the same `app` object for Gunicorn / Lambda Web Adapter.

* **Serverless runtime**

  * Built as a **Lambda container image** (`public.ecr.aws/lambda/python:3.11`).
  * Uses the **AWS Lambda Web Adapter** to forward API Gateway requests to Flask.
  * Deployed with **AWS SAM**. The SAM template provisions:

    * An **HTTP API** (`/{proxy+}` → Lambda)
    * An **S3 bucket** for artifact storage
    * IAM policies so the Lambda can read/write S3
    * (Optional) **Provisioned Concurrency** for warm starts

---

## 🔧 IT/DevOps Advantages

* **Zero changes to original repo**
  All cloud-specific logic (S3 uploads, presigned URLs) lives in `cloud_entry.py`.

* **Stateless & scalable**
  Lambdas scale horizontally with demand; artifacts live in S3, not the container.

* **Easier maintenance**
  One Lambda function, one API Gateway proxy route, one S3 bucket.
  No need to split into multiple functions unless workloads diverge.

* **Secure artifact access**
  Outputs are only accessible via short-lived presigned URLs.

* **Local + cloud parity**

  * Run locally with Docker + Gunicorn for debugging.
  * Deploy with SAM for production.

---

## 🚀 Local Testing

### Build & run container

```bash
docker build -t mtrk-backend .
docker run -it --rm -p 8080:8080 \
  -e ARTIFACT_BUCKET=my-test-bucket \
  -e AWS_DEFAULT_REGION=us-east-1 \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  mtrk-backend \
  gunicorn -b 0.0.0.0:8080 --workers 2 --threads 4 cloud_entry:app
```

Test:

```bash
curl http://localhost:8080/
```

### SAM local (simulate API Gateway + Lambda)

```bash
sam build
sam local start-api -p 8080
curl http://127.0.0.1:8080/
```

---

## 📦 Deployment

```bash
sam build
sam deploy --guided
```

The stack creates:

* **API Gateway URL** (output: `ApiUrl`)
* **S3 bucket** (output: `BucketName`)

Clients call routes like `/process`, `/convert`, `/update`, `/waveform`, etc.
Instead of downloading files directly, they receive JSON:

```json
{ "url": "https://bucket.s3.amazonaws.com/output/output.mtrk?...signature..." }
```

---

## 🔒 Security Notes

* Tighten CORS in `template.yaml` for production.
* Lock down IAM roles to least privilege.
* Consider user-specific prefixes in S3 if multi-tenant.

---

✅ In short:
We took **MTRK** as-is, added a **cloud\_entry shim** to redirect file downloads into S3, and wrapped the whole app in a **serverless, containerized Lambda** deployment for scalable, secure cloud execution.

---

Would you like me to also write a **“Quickstart for developers”** section (just 5–6 lines: clone → build → run locally → deploy) so newcomers to your lab/team can spin it up in minutes?


docker build -t mtrk-backend .


docker run -it --rm \
  -e ARTIFACT_BUCKET=my-test-bucket \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  -e AWS_DEFAULT_REGION=us-east-1 \
  -p 8080:8080 \
  mtrk-backend


curl http://localhost:8080/

curl -X POST http://localhost:8080/process -H "Content-Type: application/json" -d '{"block_to_box_objects": {...}}'


docker run -it --rm --entrypoint "" -p 8080:8080   -e ARTIFACT_BUCKET=my-test-bucket   -e AWS_DEFAULT_REGION=us-east-1   -e AWS_A
CCESS_KEY_ID=aa   -e AWS_SECRET_ACCESS_KEY=aaa   mtrk-backend   gunicorn -b 0.0.0.0:8080 --workers 2 --threads 4 cloud_entry:app