from marshmallow import Schema, fields
from marshmallow.validate import Length

class ResellerInputSchema(Schema):
    name = fields.Str(required=True, validate=Length(min=1))
    surname = fields.Str(required=True, validate=Length(min=1))
    cpf = fields.Str(required=True, validate=Length(equal=11))
    email = fields.Str(required=True, validate=Length(min=1)) #email validation can be improved using regex
    password = fields.Str(required=True, validate=Length(min=8))

class PurchaseInputSchema(Schema):
    code = fields.Int(required=True)
    amount = fields.Float(required=True)
    cpf = fields.Str(required=True, validate=Length(equal=11))
    date = fields.Str(required=True) 

class CashBackInputSchema(Schema):
    name = fields.Str(required=True, validate=Length(min=1))
    surname = fields.Str(required=True, validate=Length(min=1))
    cpf = fields.Str(required=True, validate=Length(equal=11))
    email = fields.Str(required=True, validate=Length(min=1)) #email validation can be improved using regex
    password = fields.Str(required=True, validate=Length(min=8))

class AuthInputSchema(Schema):
    email = fields.Str(required=True, validate=Length(min=1)) #email validation can be improved using regex
    password = fields.Str(required=True, validate=Length(min=8))