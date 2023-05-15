# Cycling data transformation lambda

# Build locally
1. Install sam-cli https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
2. Run
```
cd cycling-data=transformation-lambda
sam build
```

# Deploy using Pulumi
1. Install pulumi https://www.pulumi.com/docs/get-started/aws/begin/
1. Be sure that you have built locally the lmabda function. The folder should exist `cycling-data-transformation-lambda/.aws-sam/build/CyclingDataTransformationFunction` and should have the lambda package content.
2. Make sure your terminal has the right AWS credentials
3. Run
```
pulumi up
```
