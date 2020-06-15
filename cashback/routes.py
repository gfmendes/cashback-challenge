from flask import Flask
from flask_restful import Api
from cashback.controller.login_resources import LoginResource, LoginRefreshResource
from cashback.controller.business_resources import ResellerResource, PurchaseResource, PurchaseListResource, CreditResource

def init_routes(api):

  api.add_resource(LoginResource, '/cashback/login/')
  api.add_resource(LoginRefreshResource, '/cashback/login/refresh')
  api.add_resource(ResellerResource, '/cashback/reseller/')
  api.add_resource(PurchaseResource, '/cashback/purchase/')
  api.add_resource(PurchaseListResource, '/cashback/purchase/<cpf>')
  api.add_resource(CreditResource, '/cashback/credit/<cpf>')