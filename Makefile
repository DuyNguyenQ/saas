.PHONY: run-service-server
run-service-server:
	PYTHONPATH=$(PWD) gunicorn src.cfehome.wsgi:application \
	--workers 12 \
	--threads 4 \
	--worker-connections 1000 \
	--bind 0.0.0.0:8000 \
	--max-requests 1000 \
	--max-requests-jitter 50 \
	--timeout 60

.PHONY: run	
run:
	PYTHONPATH=$(PWD) python3 src/manage.py runserver 0.0.0.0:8000

.PHONY: dbshell	
dbshell:
	PYTHONPATH=$(PWD) python3 src/manage.py dbshell

.PHONY: makemigrations
makemigrations:
	PYTHONPATH=$(PWD) python3 src/manage.py makemigrations 

.PHONY: migrate
migrate:
	PYTHONPATH=$(PWD) python3 src/manage.py migrate 

.PHONY: showmigrations
showmigrations:
	PYTHONPATH=$(PWD) python3 src/manage.py showmigrations
	
.PHONY: collectstatic
collectstatic:
	PYTHONPATH=$(PWD) python3 src/manage.py collectstatic --no-input

.PHONY: superuser
superuser:
	PYTHONPATH=$(PWD) python3 src/manage.py createsuperuser

.PHONY: vendor_pull
vendor_pull:
	PYTHONPATH=$(PWD) python3 src/manage.py vendor_pull

.PHONY: update
update: 
	sudo apt-get update && \
	sudo apt-get -y upgrade && \
	pip install -r requirements.txt

