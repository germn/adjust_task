all:
	@:


install:
	poetry install


load_dataset:
	poetry run python cli.py load-dataset


run_server:
	poetry run python cli.py run-server
