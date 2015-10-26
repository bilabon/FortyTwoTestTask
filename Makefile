MANAGE=django-admin.py
SETTINGS=fortytwo_test_task.settings
ROOT_DIR=`pwd`
DATE=$(date +%Y-%m-%d)

install:
	virtualenv --no-site-packages .env
	. $(ROOT_DIR)/.env/bin/activate; pip install -r $(ROOT_DIR)/requirements.txt
	. $(ROOT_DIR)/.env/bin/activate; make syncdb
	. $(ROOT_DIR)/.env/bin/activate; make migrate

test:
	$(MAKE) clean
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) test
	flake8 --exclude '*migrations*' --ignore=F401,F403,42cc apps fortytwo_test_task

deploy:
	virtualenv --no-site-packages .env
	. $(ROOT_DIR)/.env/bin/activate; pip install -r $(ROOT_DIR)/requirements.txt
	. $(ROOT_DIR)/.env/bin/activate; make syncdb
	. $(ROOT_DIR)/.env/bin/activate; make migrate

clean:
	@echo Cleaning up *.pyc files
	-find . | grep '.pyc$$' | xargs -I {} rm {}

run:
	$(MAKE) clean
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) runserver 8004

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) syncdb --noinput

migrations:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) makemigrations

migrate:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) migrate

infomodels:
	if [ ! -d logs ]; then mkdir -p logs; fi;
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) infomodels 2> "logs/$DATE.dat"

collectstatic:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) collectstatic --noinput
.PHONY: test syncdb migrate
