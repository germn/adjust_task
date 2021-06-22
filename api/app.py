from typing import List, Optional
import datetime
import enum

from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from api import schemas
from orm.models import Metric, Channel, Country, Os
from orm.session import get_session


app = FastAPI()


def _get_sorting_type():
    fields = list(schemas.Metric.schema()["properties"])
    desc_fields = [f"-{field}" for field in fields]
    return enum.Enum("SortByFields", {field: field for field in fields + desc_fields})


SortByFields = _get_sorting_type()


@app.get("/metrics/", response_model=List[schemas.Metric])
def read_metrics(
    # Filters
    date_from: Optional[datetime.date] = Query(None, description="Date from (including date specified)"),
    date_to: Optional[datetime.date] = Query(None, description="Date to (including date specified)"),
    date_after: Optional[datetime.date] = Query(None, description="Date after (not including date specified)"),
    date_before: Optional[datetime.date] = Query(None, description="Date before (not including date specified)"),
    channel: Optional[List[Channel]] = Query(None, description="Filter by channel"),
    country: Optional[List[Country]] = Query(None, description="Filter by country"),
    os: Optional[List[Os]] = Query(None, description="Filter by OS"),
    # Sorting
    sort_by: Optional[List[SortByFields]] = Query(  # type: ignore
        None, description="Field to sort by. Use any existing field. Prepend field with a dash to sort descending."
    ),
    # Paging
    skip: int = 0,
    limit: Optional[int] = None,
    # Other
    db: Session = Depends(get_session),
):
    query = db.query(Metric)

    query = _handle_filtering(query, date_from, date_to, date_after, date_before, channel, country, os)
    query = _handle_sorting(query, sort_by)
    query = _handle_paging(query, skip, limit)

    return query.all()


def _handle_filtering(query, date_from, date_to, date_after, date_before, channel, country, os):
    if date_from:
        query = query.filter(Metric.date >= date_from)

    if date_to:
        query = query.filter(Metric.date <= date_to)

    if date_after:
        query = query.filter(Metric.date > date_after)

    if date_before:
        query = query.filter(Metric.date < date_before)

    if channel:
        query = query.filter(Metric.channel.in_(channel))

    if country:
        query = query.filter(Metric.country.in_(country))

    if os:
        query = query.filter(Metric.os.in_(os))

    return query


def _handle_sorting(query, sort_by):
    order_args = []
    for item in sort_by:
        param = item.value
        is_desc = param.startswith("-")
        attr_name = param.lstrip("-")
        attr = getattr(Metric, attr_name)
        arg = desc(attr) if is_desc else asc(attr)
        order_args.append(arg)

    if order_args:
        query = query.order_by(*order_args)

    return query


def _handle_paging(query, skip, limit):
    return query.offset(skip).limit(limit)
