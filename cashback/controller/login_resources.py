from flask_restful import Resource, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from cashback.services.reseller import ResellerService
from cashback.controller.schema_validation import AuthInputSchema, ResellerInputSchema

class LoginResource(Resource):
  def post(self):
    #data input validations
    errors = AuthInputSchema().validate(request.get_json())
    if errors: return errors, 400

    login_data = request.get_json()
    if ResellerService().validate_reseller_password(login_data):
      access_token = create_access_token(identity=login_data['email'])          
      refresh_token = create_refresh_token(identity=login_data['email'])
      return {'access_token' : access_token, 'refresh_token' : refresh_token}, 200
    else :
      print(get_raw_jwt()['jti'])
      return {'error':'incorrect email or password'}, 400

class LoginRefreshResource(Resource):
  @jwt_refresh_token_required
  def post(self):
    return {'access_token' : create_access_token(identity=get_jwt_identity())}, 200