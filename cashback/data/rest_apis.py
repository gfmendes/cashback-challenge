import requests

class CashBackAPI():
  def get_cashback_amount(self, cpf):
    url="https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf={}".format(cpf)
    head = {'Content-type':'application/json', 'token':'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm'}
    response = requests.get(url, headers=head)
    return response.json()['body']


    