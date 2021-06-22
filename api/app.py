from typing import List, Optional
import datetime

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from api import schemas
from orm import models
from orm.session import get_session


app = FastAPI()


@app.get("/metrics/", response_model=List[schemas.Metric])
def read_metrics(
    # Filters
    date_from: Optional[datetime.date] = None,
    date_to: Optional[datetime.date] = None,
    # Paging
    skip: int = 0,
    limit: Optional[int] = None,
    # Other
    db: Session = Depends(get_session),
):
    query = db.query(models.Metric)

    # Filters
    if date_from:
        query = query.filter(models.Metric.date >= date_from)

    if date_to:
        query = query.filter(models.Metric.date <= date_to)

    # Paging
    query = query.offset(skip).limit(limit)

    return query.all()
