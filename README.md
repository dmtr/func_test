For development:
* docker-compose -f docker-compose.yml build
* docker-compose -f docker-compose.yml up -d
* docker-compose run web python func_test/manage.py migrate 

Run tests:
* docker-compose run web python func_test/manage.py test funcapp.tests

For production:
* docker-compose -f docker-compose.prod.yml build
* docker-compose -f docker-compose.prod.yml up -d

