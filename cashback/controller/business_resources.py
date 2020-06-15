from flask_restful import Resource, request
from flask_jwt_extended import  jwt_required
from cashback.controller.schema_validation import CashBackInputSchema,PurchaseInputSchema,ResellerInputSchema
from cashback.services.purchase import PurchaseService
from cashback.services.reseller import ResellerService

class ResellerResource(Resource):
  def post(self):
    #data input validations
    errors = ResellerInputSchema().validate(request.get_json())
    if errors: return str(errors), 400

    result = ResellerService().add_reseller(request.get_json())
    return (result, 400) if 'error' in result.keys() else (result, 201)

class CreditResource(Resource):
  @jwt_required
  def get(self, cpf):
    return PurchaseService().get_cashback_amount(cpf), 200

class PurchaseResource(Resource):
  @jwt_required
  def post(self):
    #data input validations
    errors = PurchaseInputSchema().validate(request.get_json())
    if errors: return str(errors), 400

    result = PurchaseService().add_purchase(request.get_json())
    return (result, 400) if 'error' in result.keys() else (result, 201)

class PurchaseListResource(Resource):
  @jwt_required
  def get(self, cpf):
    return PurchaseService().list_current_month_purchases(cpf), 200