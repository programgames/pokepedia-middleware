local_config = --settings=config.local

.PHONY: all pokeapi

all: pokeapi

.SILENT:

help:
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  # Install base requirements to run project
	pip install -r requirements.txt

dev-install:  # Install developer requirements + base requirements
	pip install -r test-requirements.txt

setup:  # Set up the project database
	python manage.py migrate ${local_config}

build-db:  # Build database
	echo "from data.v2.build import build_all; build_all()" | python manage.py shell ${local_config}

wipe-sqlite-db:  # Delete's the project database
	rm -rf db.sqlite3

serve:  # Run the project locally
	python manage.py runserver ${local_config}

test:  # Run tests
	python manage.py test ${local_config}

clean:  # Remove any pyc files
	find . -type f -name '*.pyc' -delete

migrate:  # Run any outstanding migrations
	python manage.py migrate ${local_config}

make-migrations:  # Create migrations files if schema has changed
	python manage.py makemigrations ${local_config}

shell:  # Load a shell
	python manage.py shell ${local_config}

docker-setup:
	$(MAKE) -C pokeapi docker-setup

docker-build-db:
	$(MAKE) -C pokeapi docker-build-db