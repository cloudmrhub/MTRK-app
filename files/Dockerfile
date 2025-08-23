# Dockerfile
FROM public.ecr.aws/lambda/python:3.11

# (Optional) system deps if needed for scientific libs
# RUN yum -y install gcc gcc-c++ make && yum clean all

# Install curl (needed to fetch the Web Adapter)
RUN yum -y install curl && yum clean all

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Download AWS Lambda Web Adapter (latest) and make it executable

COPY aws-lambda-adapter /opt/extensions/aws-lambda-adapter
RUN chmod +x /opt/extensions/aws-lambda-adapter

# Your app
COPY . /var/task
WORKDIR /var/task

# Web adapter env
ENV PORT=8080 AWS_LWA_PORT=8080

# Start Flask via gunicorn through the shim entry (cloud_entry:app)
CMD ["sh","-c","gunicorn -b 0.0.0.0:${PORT} --workers 2 --threads 4 cloud_entry:app"]
