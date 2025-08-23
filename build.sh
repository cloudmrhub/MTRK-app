wget https://github.com/awslabs/aws-lambda-web-adapter/releases/tag/v0.9.1/downloads/aws-lambda-adapter -o files/aws-lambda-adapter

git clone https://github.com/mtrk-dev/mtrk_designer_gui
cd mtrk_designer_gui
cd app
cp ../requirements.txt .
cp ../../files/* .
git clone https://github.com/mtrk-dev/mtrk_designer_api
cd ..


sam build --profile nyu
sam deploy --guided --profile nyu