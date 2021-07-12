# Flask + Lambda + APIGateway Template 

This document refered to https://www.serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb

## Instration

Install npm packages

```bash
# At project root dir
npm install
```

Install python packages

```bash
pip install -r requirement.txt
```



## Work on local

Set environment variables

```bash
cp env.sh.sample env.sh
vi env.sh
```

```bash
export AWS_PROFILE="your-profile-name"
export AWS_REGION="ap-northeast-1"
export BASE_URL="https://xxxxxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev"
export USERS_TABLE="users-table-dev"
export IS_OFFLINE=1
```

Execute below command

````bash
sls wsgi serve
````

Request [http://127.0.0.1:5000](http://127.0.0.1:5000/hoge)



## Deploy to Lambda

Execute below command

````bash
export AWS_PROFILE="your-profile-name"
export AWS_REGION="ap-northeast-1"
sls deploy
````

Request https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev

