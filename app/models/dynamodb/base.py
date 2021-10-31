import os
import boto3


class Base():
    __abstract__ = True

    IS_LOCAL = bool(os.environ.get('IS_LOCAL'))
    PRJ_PREFIX = os.environ['PRJ_PREFIX']
    ACCEPT_SERVICE_IDS = os.environ.get('ACCEPT_SERVICE_IDS', '').split(',')


    @classmethod
    def connect_dynamodb(self):
        if self.IS_LOCAL:
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
        else:
            dynamodb = boto3.resource('dynamodb')
        return dynamodb


    @classmethod
    def get_table(self, table_name=None):
        dynamodb = self.connect_dynamodb()
        table_name = self.get_table_name()
        return dynamodb.Table(table_name)


    @classmethod
    def get_table_name(self):
        return '-'.join([self.PRJ_PREFIX, self.table_name])


    @classmethod
    def batch_get_items(self, keys):
        dynamodb = self.connect_dynamodb()
        table_name = self.get_table_name()
        res = dynamodb.batch_get_item(
            RequestItems={
                table_name: {
                    'Keys': keys,
                    'ConsistentRead': True
                }
            },
            ReturnConsumedCapacity='TOTAL'
        )
        return res['Responses'][table_name]