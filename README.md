# Proposed solution to Boticario's backend challenge.

## Modules description:
<pre>
<b>cashback/</b>
<b>|--controller</b>
   <b>|--business_resources.py</b> - Endpoints related to cashback business logic such as add reseller, list purchases, etc.
   <b>|--login_resources.py</b> - Endpoints related to login and auth token data.
   <b>|--schema_validation.py</b> - Json schema validations for app endpoints.
<b>|--data/</b>
   <b>|--data_access.py</b> - Abstraction layer between services and data access objects. Data objects changes are transparent to services modules.
   <b>|--mongo_collections.py</b> - Contains logic to access MongoDb collections.
   <b>|--rest_api.py</b> - Contains logic to access external APIs endpoints.
<b>|--services/</b>  
   <b>|--purchase.py</b> - Address purchase business logic. Service layer implementation is independent of frameworks such flask, django, pymongo, etc.
   <b>|--reseller.py</b> - Address reseller business logic. Service layer implementation is independent of frameworks such flask, django, pymongo, etc.
<b>|--app.py</b> - Contains app configs and flask run function.
<b>|--routes.py</b> - Define cachback app routes.  
<b>tests/</b>  
<b>|--integration/</b>
   <b>|--test_routes.py</b> - Automated end-to-end tests.
<b>|--unit/</b>
   <b>|--services/</b>
     <b>|--test_purchase.py</b> - Purchase service unit tests.
     <b>|--test_reseller.py</b> - Reseller service unit tests.
</pre>

## Configuring dev environment - pipenv needed: https://pypi.org/project/pipenv/
> pipenv --python 3  
> pipenv install  
> pipenv shell  

## Running the application:
#Unix
> export FLASK_APP=cashback/app.py  
> flask run

#Windows cmd
> set FLASK_APP=cashback/app.py  
> flask run

#Windows PowerShell
> $env:FLASK_APP="cashback/app.py"  
> flask run

## Running all UT and IT tests:
> python -m unittest discover
  
## Run UT tests from services layer:
> python -m unittest tests/unit/services/test_purchase.py  
> python -m unittest tests/unit/services/test_reseller.py  

## Run IT tests:
> python -m unittest tests/integration/test_routes.py   