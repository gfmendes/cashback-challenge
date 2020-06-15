import logging
import datetime
from cashback.data.data_access import ResellerData, PurchaseData, CashBackData

ERROR_RESELLER_CPF_NOT_EXISTS = {'error':'reseller cpf does not exists'}
PRE_APPROVED_RESELLERS = ['15350946056'] #This data should be externalized in an API call or database

class PurchaseService():
  def __init__(self, *args, **kwargs):
    self.log = logging.getLogger(self.__class__.__name__)
  
  def add_purchase(self, purchase):
    self.log.info("add_purchase::Adding purchase=%s", purchase)
    errors = self._validate_purchase(purchase)
    if errors : return errors

    purchase['status'] = 'Approved' if purchase['cpf'] in PRE_APPROVED_RESELLERS else 'Validating'
    self.log.info("add_purchase::Purchase status=%s", purchase['status'])
    return PurchaseData().add_purchase(purchase)
    
  def _validate_purchase(self, purchase):
    cpf_check = ResellerData().find_reseller({"cpf" : purchase['cpf']})
    self.log.info("_validate_purchase::find_reseller return=%s", cpf_check)
   
    if not cpf_check: 
      self.log.error("_validate_purchase::Reseller CPF=%s not found.",purchase['cpf'])
      return ERROR_RESELLER_CPF_NOT_EXISTS

  def list_current_month_purchases(self, cpf):
    self.log.info("list_current_month_purchases::Listing monthly purchases of cpf=%s", cpf)
    today = datetime.date.today()
    purchases = PurchaseData().find_monthly_purchases({"cpf" : cpf, "month" : today.month, "year" : today.year})
    self.log.info("list_current_month_purchases::find_monthly_purchases return=%s", purchases)
    
    total_amount = sum(p["amount"] for p in purchases)
    self.log.info("list_current_month_purchases::total amount purchases=%f", total_amount )

    for p in purchases: 
      p['cash_back'] = self.__apply_cache_back(total_amount, p['amount'])
      self.log.info("list_current_month_purchases::For purchase=%f, cash back=%f", p['amount'], p['cash_back'])  
    return purchases
  
  def __apply_cache_back(self, total_amount, amount):
    if total_amount <= 1000 : return amount * 0.1
    elif total_amount <= 1500 : return amount * 0.15  
    else: return amount * 0.2 

  def get_cashback_amount(self, cpf):
    self.log.info("get_cashback_amount::retrieving cashback amount from cpf=%s", cpf)
    return CashBackData().get_cashback_amount(cpf)
