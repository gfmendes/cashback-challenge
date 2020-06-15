import json
import pymongo

#Database URL, user and pass should be externalized. 
client = pymongo.MongoClient("mongodb+srv://boticario-dev:Dummypasswd@cluster0-zmuno.mongodb.net/boticario?retryWrites=true&w=majority")
database = client.boticario

class PurchaseCollection():
  def add(self, purchase):
    database.purchase.insert_one(purchase)
    purchase.pop("_id", None)
    return purchase

  def find_all_per_month(self, params):
    
    result = database.purchase.find(
      { "$and": [  
          {"$expr": { "$eq": [{ "$year": [{ "$dateFromString": { "dateString" : "$date" }}]}, params['year']]}},
          {"$expr": { "$eq": [{ "$month": [{ "$dateFromString": { "dateString" : "$date" }}]}, params['month']]}},
          { "cpf" : params['cpf']}
      ]}, {'_id': False})
    return list(result)

class ResellerCollection():
  def add(self, reseller):     
    database.reseller.insert_one(reseller)
    reseller.pop("_id", None)
    return reseller
    
  def find_one(self, params):     
    return database.reseller.find_one(params)
