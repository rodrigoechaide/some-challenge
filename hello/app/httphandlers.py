import json

from database import exists, daysToBirthday, insert_user
from validators import username_validation, dateOfBirth_validation

def get_handler(event):
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

def put_handler(event):
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
      elif not dateOfBirth_validation(dateOfBirth):
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