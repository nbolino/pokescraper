import boto3
from io import StringIO
import os, time
import json, decimal

# credit: https://github.com/aaronglang/cl_scraper/blob/master/src/utils.py

class Utils:
    def saveResults(self, df, site):
        """ save parsed scrape results """
        ts = int(time.time())
        if os.environ['ENV'] == 'dev':
            dirname = os.getcwd()
            df.to_csv(f'{dirname}/results/{site}_{ts}_results.csv')
        else:
            # self.sendToS3(df, site, ts)
            self.sendToDynamo(df)


    def sendToDynamo(self, df):
        # get env variables if dev environment (local)
        if os.environ['ENV'] == 'local':
            s3_secret = os.environ['S3_SECRET']
            s3_key = os.environ['S3_KEY']
            region = os.environ['AWS_REGION']
            ddb_resource = boto3.resource('dynamodb', aws_access_key_id=s3_key, aws_secret_access_key=s3_secret, region_name=region)
        else:
            ddb_resource = boto3.resource('dynamodb')
        table = ddb_resource.Table('pokelex_data')
        print('sending to ddb...')
        with table.batch_writer() as batch:
            for _ , row in df.iterrows():
                jsonStr = json.loads(row.to_json(), parse_float=decimal.Decimal)
                batch.put_item(jsonStr)


    def sendToS3(self, df, site, ts):
        # get variable names
        s3_bucket = os.environ['S3_BUCKET']
        # get env variables if dev environment (local)
        if os.environ['ENV'] == 'local':
            s3_secret = os.environ['S3_SECRET']
            s3_key = os.environ['S3_KEY']
            s3_resource = boto3.resource('s3', aws_access_key_id=s3_key, aws_secret_access_key=s3_secret)
            # s3_client = boto3.client('s3', aws_access_key_id=s3_key, aws_secret_access_key=s3_secret)
        else:
            s3_resource = boto3.resource('s3')
            # s3_client = boto3.client('s3')
        
        # create csv buffer to send to S3
        csv_buffer = StringIO()
        filename = f'{site}_{ts}_results.csv'
        df.to_csv(csv_buffer)

        # send to S3
        print('sending to s3...')
        s3_resource.Object(s3_bucket, filename).put(Body=csv_buffer.getvalue())

    """
    def folderExists(self, client, bucket, folder):
        res = client.list_objects_v2(Bucket=bucket, Prefix=folder)
        if res['KeyCount'] > 0:
            return True
        else:
            client.put_object(Bucket=bucket, Body='', Key=folder)
    """