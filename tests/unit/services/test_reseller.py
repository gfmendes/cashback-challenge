import unittest, hashlib
from mock import MagicMock
from cashback.services.reseller import ResellerService
from cashback.data.data_access import ResellerData

class ResellerServiceTest(unittest.TestCase) :
    
  def test_when_add_new_customer_then_success(self):
    #Given
    reseller = {"cpf":"15350946051", "name":"John", "surname":"Galt", "email":"galt@gmail.com", "password":"12345678"}
    #mocking data layer
    ResellerData.find_reseller = MagicMock(return_value={})
    ResellerData.add_reseller = MagicMock(return_value=reseller)
    #when
    result = ResellerService().add_reseller(reseller)
    #then
    self.assertIn('cpf', result.keys())
    self.assertIn('email', result.keys())

  def test_when_add_existent_customer_then_error(self):
    #Given
    reseller = {"cpf":"15350946051", "name":"John", "surname":"Galt", "email":"galt@gmail.com", "password":"12345678"}
    #mocking data layer
    ResellerData.find_reseller = MagicMock(return_value={'cpf':'15350946051'})
    ResellerData.add_reseller = MagicMock(return_value=reseller)
    #when
    result = ResellerService().add_reseller(reseller)
    #then
    self.assertIn('error', result.keys())
 
  def test_when_login_info_ok_then_return_true(self):
    #Given
    login_data = {"email":"galt@gmail.com", "password":"12345678"}
    #mocking data layer
    hashed_password = hashlib.sha256('12345678'.encode('utf8')).hexdigest()
    ResellerData.find_reseller = MagicMock(return_value={'password':hashed_password})
    #when
    result = ResellerService().validate_reseller_password(login_data)
    #then
    self.assertTrue(result)
  
  def test_when_login_info_nok_then_return_false(self):
    #Given
    login_data = {"email":"galt@gmail.com", "password":"87654321"}
    #mocking data layer
    hashed_password = hashlib.sha256('12345678'.encode('utf8')).hexdigest()
    ResellerData.find_reseller = MagicMock(return_value={'password':hashed_password})
    #when
    result = ResellerService().validate_reseller_password(login_data)
    #then
    self.assertFalse(result)