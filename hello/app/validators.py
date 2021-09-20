import datetime

def username_validation(username):
  return username.isalpha()

def dateOfBirth_validation(dateOfBirth):
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