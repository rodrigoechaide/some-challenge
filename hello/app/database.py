import os
import boto3
import datetime

def dynamodb_connector():
  ENVIRONMENT = os.getenv("ENVIRONMENT")
  TABLE_NAME = os.getenv("TABLE_NAME")
  if ENVIRONMENT == "local":
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://dynamodb:8000")
  else:
    dynamodb = boto3.resource('dynamodb')
  return dynamodb.Table(TABLE_NAME)

def insert_user(username, dateOfBirth):
  try:
    dynamodb_table = dynamodb_connector()
    dynamodb_table.put_item(Item={'username': username, 'dateOfBirth': dateOfBirth})
    return True
  except:
    return False

def exists(username):
  dynamodb_table = dynamodb_connector()
  try:
    response = dynamodb_table.get_item(Key={'username': username})
    if 'Item' in response.keys():
      return True
    else:
      return False
  except:
    return False

def getBirthday(username):
  dynamodb_table = dynamodb_connector()
  response = dynamodb_table.get_item(Key={'username': username})
  return datetime.datetime.strptime(response['Item']['dateOfBirth'], '%Y-%m-%d')

def daysToBirthday(username):
  # Get the current date in datetime format removing milliseconds and with 0 hours, minutes and seconds
  today = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + '-00-00-00', '%Y-%m-%d-%H-%M-%S')
  # Get the date of birth of the username in datetime format
  dateOfBirth = getBirthday(username)
  # Get the birthday of the username in this year in datetime format
  nextBirthday = datetime.datetime.strptime(today.strftime("%Y") + "-" + dateOfBirth.strftime("%m-%d"), '%Y-%m-%d')
  remainingDays = (nextBirthday - today).days
  if nextBirthday == today:
    return 0
  elif nextBirthday > today:
    return remainingDays
  else:
    return (365 + remainingDays)