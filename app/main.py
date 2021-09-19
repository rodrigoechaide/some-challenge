import json
import datetime
import os
import boto3

def dynamodb_connector():
  '''Function that returns an object with the DynamoDB table to interact with'''

  ENVIRONMENT = os.getenv("ENVIRONMENT")
  TABLE_NAME = os.getenv("TABLE_NAME")

  if ENVIRONMENT == "local":
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://dynamodb:8000")
  else:
    dynamodb = boto3.resource('dynamodb')
  return dynamodb.Table(TABLE_NAME)

def username_validation(username):
  '''Function that validates that the username only contains letters. 
  Returns True if the username is valid and False if it is not'''

  return username.isalpha()

def dateOfbirth_validation(dateOfBirth):
  '''Function that validates if the date of birth of the user is a date before Today and if the format 
  is correct (YYYY-MM-DD). Returns True if the date of birth is valid and False if it is not.'''

  # Get the current date in datetime format removing milliseconds and with 0 hours, minutes and seconds
  today = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + '-00-00-00', '%Y-%m-%d-%H-%M-%S')
  try:
    # Try to create dateOfBirth object in datetime format removing milliseconds and with 0 hours, minutes and seconds
    # If the dateOfBirth does not complies with the format YYYY-MM-DD this will fail
    dateOfBirth = datetime.datetime.strptime(dateOfBirth + '-00-00-00', '%Y-%m-%d-%H-%M-%S')
    if today == dateOfBirth:
      return False
    else:
      return True
  except:
    return False

def insert_user(username, dateOfBirth):
  '''Fuction that inserts the username and the date of birth into the Database. Returns 
  True if the instert was successful and False if it was not.'''

  try:
    dynamodb_table = dynamodb_connector()
    dynamodb_table.put_item(Item={'username': username, 'dateOfBirth': dateOfBirth})
    return True
  except:
    return False

def exists(username):
  '''Returns True if the user exists in the database
  otherwise it returns False'''

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
  '''Return the date of birth of a given username in datetime format'''

  dynamodb_table = dynamodb_connector()
  response = dynamodb_table.get_item(Key={'username': username})
  return datetime.datetime.strptime(response['Item']['dateOfBirth'], '%Y-%m-%d')

def daysToBirthday(username):
  '''Return the remaining days for the birthday of a given username
  or zero if the birthday is today'''

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

def lambda_handler(event, context):
  try:
    httpMethod = event['httpMethod']
    if httpMethod == "GET":
      try:
        username = event['pathParameters']['username']
        if exists(username):
          days = daysToBirthday(username)
          if days != 0:
            message = f'Hello {username}! Your birthday is in {days} day(s)'
          else:
            message = f'Hello {username}! Happy Birthday!'
          return {"statusCode": 200, "body": json.dumps({"message": message})}
        else:
          message = "User does not exists in the database."
          return {"statusCode": 404, "body": json.dumps({"message": message})}
      except:
        message = "Something went wrong. Please try again."
        return {"statusCode": 500, "body": json.dumps({"message": message})}
    elif httpMethod == "PUT":
      try:
        username = event['pathParameters']['username']
        dateOfBirth = json.loads(event['body'])['dateOfBirth']
        if exists(username):
          message = "User already exists in the database."
          return {"statusCode": 400, "body": json.dumps({"message": message})}
        else:
          if not username_validation(username):
            message = "The username is not valid. It must only contain letters."
            return {"statusCode": 400, "body": json.dumps({"message": message})}            
          elif not dateOfbirth_validation(dateOfBirth):
            message = "The day of birth is not valid. Check that is not Today and that complies with the format YYYY-MM-DD"
            return {"statusCode": 400, "body": json.dumps({"message": message})}
          else:
            if insert_user(username, dateOfBirth):
              return {"statusCode": 204, "body": json.dumps({})}
            else:
              message = "Something went when inserting the user in the Database. Please try again."
              return {"statusCode": 500, "body": json.dumps({"message": message})}
      except:
        message = "Something went wrong. Please try again."
        return {"statusCode": 500, "body": json.dumps({"message": message})}
    else:
      message = "HTTP Method not suported. Please try again."
      return {"statusCode": 500, "body": json.dumps({"message": message})}
  except:
    message = "Something went  wrong. Please try again."
    return {"statusCode": 500, "body": json.dumps({"message": message})}