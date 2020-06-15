import requests
import ast
import logging

class CashBackAPI():
  def get_cashback_amount(self, cpf):
    url="https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf=12312312323"
    head = {'Content-type':'application/json', 'token':'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm'}
    response = requests.get(url, headers=head)
    return ast.literal_eval(response.text)['body']


    