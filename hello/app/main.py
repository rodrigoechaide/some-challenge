import json

from httphandlers import get_handler, put_handler

def lambda_handler(event, context):
  try:
    httpMethod = event['httpMethod']
    if httpMethod == "GET":
      response = get_handler(event)
      return response
    elif httpMethod == "PUT":
      response = put_handler(event)
      return response
    else:
      message = "HTTP Method not suported. Please try again."
      return {"statusCode": 405, "body": json.dumps({"message": message})}
  except:
    message = "HTTP Method not suported. Please try again."
    return {"statusCode": 405, "body": json.dumps({"message": message})}