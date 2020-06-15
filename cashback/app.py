import logging
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from cashback.routes import init_routes

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

#jwt config
app.config['JWT_SECRET_KEY'] = 'secret-string'
jwt = JWTManager(app)

#routes
api = Api(app)
init_routes(api)

#logging (examples of use in service modules)
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    app.run(debug=True)