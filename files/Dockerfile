FROM public.ecr.aws/lambda/python:3.11
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD https://github.com/awslabs/aws-lambda-web-adapter/releases/latest/download/aws-lambda-adapter /opt/extensions/aws-lambda-adapter
RUN chmod +x /opt/extensions/aws-lambda-adapter
COPY . /var/task
WORKDIR /var/task
ENV PORT=8080 AWS_LWA_PORT=8080
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} --workers 2 --threads 4 cloud_entry:app"]
