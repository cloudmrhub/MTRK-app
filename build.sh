wget -P files https://github.com/awslabs/aws-lambda-web-adapter/releases/tag/v0.9.1/downloads/aws-lambda-adapter
git clone https://github.com/mtrk-dev/mtrk_designer_gui
cd mtrk_designer_gui
cd app
cp ../requirements.txt .
cp ../../files/* .
git clone https://github.com/mtrk-dev/mtrk_designer_api

echo $(pwd)
docker build -t mtrk-backend .
docker run -it --rm --entrypoint "" -p 8080:8080   -e ARTIFACT_BUCKET=my-test-bucket   -e AWS_DEFAULT_REGION=us-east-1   -e AWS_ACCESS_KEY_ID=aa   -e AWS_SECRET_ACCESS_KEY=aaa   mtrk-backend   gunicorn -b 0.0.0.0:8080 --workers 2 --threads 4 cloud_entry:app
xdg-open "http://localhost:8080"


#sam build --profile nyu
#sam deploy --guided --profile nyu