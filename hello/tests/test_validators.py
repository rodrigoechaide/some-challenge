import unittest
import sys
import datetime

sys.path.append('../app')

from validators import username_validation, dateOfBirth_validation

class TestUsernameValidation(unittest.TestCase):
  def test_usernme_letters(self):
    """
    Test that returned True if the username contains only letters
    """
    data = "usertest"
    result = username_validation(data)
    self.assertEqual(result, True)
  def test_username_numbers(self):
    """
    Test that returns False if the username contains numbers
    """
    data = "usertest21"
    result = username_validation(data)
    self.assertEqual(result, False)
  def test_username_special_characters(self):
    """
    Test that returns False if the username contains numbers
    """
    data = "@user.test"
    result = username_validation(data)
    self.assertEqual(result, False)

class TestDateOfBirthValidation(unittest.TestCase):
  def test_valid_date(self):
    """
    Test that returned True if the date is not today and is valid.
    """
    data = "1989-11-29"
    result = dateOfBirth_validation(data)
    self.assertEqual(result, True)
  def test_date_today(self):
    """
    Test that returns False if the date is today
    """
    data = datetime.datetime.now().strftime("%Y-%m-%d")
    result = dateOfBirth_validation(data)
    self.assertEqual(result, False)
  def test_invalid_date(self):
    """
    Test that returns False if the date is not valid
    """
    data = "88-10-11"
    result = dateOfBirth_validation(data)
    self.assertEqual(result, False)

if __name__ == '__main__':
  unittest.main()

