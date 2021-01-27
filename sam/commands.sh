# Create an s3 bucket

aws s3 mb s3://mjcloudgurusam

# Create cloud formation package

aws cloudformation package --s3-bucket mjcloudgurusam --template-file template.yaml  \
--output-template-file gen/template-generate-yaml

# deploy generate template

aws cloudformation deploy  --tempate-file gen/template-generate.yaml --stack-name hello-world
