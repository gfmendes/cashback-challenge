import unittest
import json
from cashback.app import app
import cashback.data.mongo_collections as mongo_collections

#Integration/automated tests 
class ResellerIntegrationTest(unittest.TestCase) :

  def setUp(self):
    self.app = app.test_client()
    #setting up mongo to point to a test database
    mongo_collections.database = mongo_collections.client.boticario_tests

  def test_add_new_reseller(self):
    #Given
    payload = json.dumps({"cpf":"15138291498","name":"John","surname":"Galt","email":"snow@email.com","password":"12345678"})
    #When
    response = self._add_reseller_request(payload)
    #Then
    self.assertEqual(201, response.status_code)
    self.assertEqual("15138291498", response.json['cpf'])

  def test_add_existent_email_reseller(self):
    #Given
    payload1 = json.dumps({"cpf":"15138291477", "name":"John", "surname":"Galt", "email":"snow@email.com", "password":"12345678"})
    payload2 = json.dumps({"cpf":"15138291498", "name":"John", "surname":"Snow", "email":"snow@email.com", "password":"12345678"})
    #When
    self._add_reseller_request(payload1) #Adding first time
    response = response = self._add_reseller_request(payload2) #Adding second time
    #Then
    self.assertEqual(400, response.status_code)
    self.assertEqual("email exists", response.json['error'])

  def test_add_existent_cpf_reseller(self):
    #Given
    payload1 = json.dumps({"cpf":"15138291498","name":"John","surname":"Galt","email":"galt@email.com","password":"12345678"})
    payload2 = json.dumps({"cpf":"15138291498","name":"John","surname":"Snow","email":"snow@email.com","password":"12345678"})
    #When
    self._add_reseller_request(payload1) #Adding first time
    response = response = self._add_reseller_request(payload2) #Adding second time
    #Then
    self.assertEqual(400, response.status_code)
    self.assertEqual("cpf exists", response.json['error'])

  def test_get_cash_back_credit(self):
    #Given
    payload_add_reseller = json.dumps({"cpf":"15138291498","name":"John","surname":"Galt","email":"snow@email.com","password":"12345678"})
    payload_login = json.dumps({"email":"snow@email.com","password":"12345678"}) 
    #When
    self._add_reseller_request(payload_add_reseller)
    access_tokens = self._login_request(payload_login)
    response = self._get_cashback_credit_request('15138291498', access_tokens)
    #Then
    self.assertEqual(200, response.status_code)
    self.assertIn("credit", response.json.keys())

  def test_add_purchase(self):
    #Given
    payload_add_reseller = json.dumps({"cpf":"15138291498","name":"John","surname":"Galt","email":"snow@email.com","password":"12345678"})
    payload_add_purchase = json.dumps({"cpf":"15138291498", "amount":700.01, "code":999, "date":"2021-06-08"})
    payload_login = json.dumps({"email":"snow@email.com","password":"12345678"}) 
    #When
    self._add_reseller_request(payload_add_reseller)
    access_tokens = self._login_request(payload_login)
    response = self._add_purchase_request(payload_add_purchase, access_tokens)
    #Then
    self.assertEqual(201, response.status_code)
    
  def test_add_and_list_purchases(self):
    #Given
    payload_add_reseller = json.dumps({"cpf":"15138291498","name":"John","surname":"Galt","email":"snow@email.com","password":"12345678"})
    payload_add_purchase = json.dumps({"cpf":"15138291498", "amount":700.01, "code":999, "date":"2020-06-08"})
    payload_login = json.dumps({"email":"snow@email.com","password":"12345678"}) 
    #When
    self._add_reseller_request(payload_add_reseller)
    access_tokens = self._login_request(payload_login)
    self._add_purchase_request(payload_add_purchase, access_tokens)
    self._add_purchase_request(payload_add_purchase, access_tokens)
    response = self._list_purchases_request('15138291498', access_tokens)
    #Then
    self.assertEqual(200, response.status_code)
    for p in response.json:
      self.assertEqual(700.01, p['amount'])
      self.assertEqual((700.01 * 0.15), p['cash_back'])

  def _login_request(self, payload):
    return self.app.post('/cashback/login/', headers={'Content-Type': 'application/json'}, data=payload)

  def _add_reseller_request(self, payload):
    return self.app.post('/cashback/reseller/', headers={'Content-Type': 'application/json'}, data=payload)

  def _add_purchase_request(self, payload, access_tokens):
    head={
      'Content-Type': 'application/json' ,
      'Authorization' : 'Bearer '+ access_tokens.json['access_token']
    }
    return self.app.post('/cashback/purchase/', headers=head, data=payload)
  
  def _list_purchases_request(self, cpf, access_tokens):
    head={
      'Content-Type': 'application/json' ,
      'Authorization' : 'Bearer '+ access_tokens.json['access_token']
    }
    route = '/cashback/purchase/'+cpf
    return self.app.get(route, headers=head)
  
  def _get_cashback_credit_request(self, cpf, access_tokens):
    head={
      'Content-Type': 'application/json' ,
      'Authorization' : 'Bearer '+ access_tokens.json['access_token']
    }
    route = '/cashback/credit/'+cpf
    return self.app.get(route, headers=head)

  def tearDown(self):
    #removing all testcase data from mongo test database
    for collection in mongo_collections.database.list_collection_names():
      mongo_collections.database.drop_collection(collection)