import unittest
import boto3
import sys
import os
from moto import mock_dynamodb2

sys.path.append('../app')

from database import dynamodb_connector, insert_user, exists, getBirthday, daysToBirthday

@mock_dynamodb2
class TestDatabaseFunctions(unittest.TestCase):

  def setUp(self):
    self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    self.table = self.dynamodb.create_table(
        TableName='birthdays_table',
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

  def tearDown(self):
    self.table.delete()
    self.dynamodb=None

  def test_table_exists(self):
    def test_table_exists(self):
      self.assertIn('birthday_table', self.table.name)

if __name__ == '__main__':
  unittest.main()