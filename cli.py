import click
import pandas
import uvicorn

from config import DATASET_PATH, SERVER_HOST, SERVER_PORT
from orm import models
from orm.session import engine


@click.group()
def cli():
    pass


@cli.command()
def load_dataset():
    df = pandas.read_csv(DATASET_PATH)
    df.to_sql(con=engine, name=models.Metric.__tablename__, index_label="metric_id", if_exists="replace")


@cli.command()
def run_server():
    models.Base.metadata.create_all(bind=engine)
    uvicorn.run("api.app:app", host=SERVER_HOST, port=SERVER_PORT, reload=True, workers=2)


if __name__ == "__main__":
    cli()
