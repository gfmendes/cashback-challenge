from cashback.data.mongo_collections import ResellerCollection, PurchaseCollection
from cashback.data.rest_apis import CashBackAPI

#This module is a layer of abstraction between services and data access objects
#this way it is possible to change how data is fetch without change service modules
class PurchaseData():
  def add_purchase(self, purchase):
    return PurchaseCollection().add(purchase)
  
  def find_monthly_purchases(self, params):
    return PurchaseCollection().find_all_per_month(params)

class ResellerData():
  def add_reseller(self, reseller):
    return ResellerCollection().add(reseller)
  
  def find_reseller(self, params):
    return ResellerCollection().find_one(params)

class CashBackData():
  def get_cashback_amount(self, params):
    return CashBackAPI().get_cashback_amount(params)