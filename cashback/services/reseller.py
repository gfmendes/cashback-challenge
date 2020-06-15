import json
import hashlib
import logging
from cashback.data.data_access import ResellerData

ERROR_CPF_EXISTS = {"error" : "cpf exists"}
ERROR_EMAIL_EXISTS = {"error" : "email exists"}

class ResellerService():
  def __init__(self, *args, **kwargs):
    self.log = logging.getLogger(self.__class__.__name__)
  
  def add_reseller(self, reseller):
    self.log.info("add_reseller::Adding reseller=%s", reseller)
    errors = self._check_reseller_exists(reseller)
    if errors: return errors
    
    reseller['password'] = self._hash_password(reseller['password'])
    ResellerData().add_reseller(reseller)
    self.log.info("add_reseller::Reseller added=%s", reseller)
    return reseller
        
  def _check_reseller_exists(self, reseller):
    email_check = ResellerData().find_reseller({"email" : reseller['email']})
    if email_check: 
      self.log.error("_check_reseller_exists::Reseller email=%s already exists.",reseller['email']) 
      return ERROR_EMAIL_EXISTS

    cpf_check = ResellerData().find_reseller({"cpf" : reseller['cpf']})
    if cpf_check:
      self.log.error("_check_reseller_exists::Reseller CPF=%s already exists.",reseller['cpf']) 
      return ERROR_CPF_EXISTS

  def validate_reseller_password(self, login_data):
    self.log.info("validate_reseller_password::Validating login=%s", login_data['email']) #do not log password as it is sensitive data
    password = self._hash_password(login_data['password'])
    reseller = ResellerData().find_reseller({"email" : login_data['email']})
    return True if (reseller and reseller['password'] == password) else False

  def _hash_password(self, password) :
          return hashlib.sha256(password.encode('utf8')).hexdigest()

