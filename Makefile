all:
	@:


install:
	poetry install


install_hooks:
	poetry run pre-commit install


run_hooks:
	poetry run pre-commit run --all-files


load_dataset:
	poetry run python cli.py load-dataset


run_server:
	poetry run python cli.py run-server
