from typing import List, Optional
import datetime

from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, case, inspect

from api import schemas
from orm.models import Metric, Channel, Country, Os
from orm.session import get_session


app = FastAPI()


@app.get("/metrics/", response_model=List[schemas.Metric], response_model_exclude_unset=True)
def read_metrics(
    # Grouping
    group_by: Optional[List[schemas.GroupByFields]] = Query(None, description="Field to group by"),
    # Sorting
    sort_by: Optional[List[schemas.SortByFields]] = Query(
        None, description="Field to sort by. Prepend field with a dash to sort descending."
    ),
    # Filters
    date_from: Optional[datetime.date] = Query(None, description="Date from (including date specified)"),
    date_to: Optional[datetime.date] = Query(None, description="Date to (including date specified)"),
    date_after: Optional[datetime.date] = Query(None, description="Date after (not including date specified)"),
    date_before: Optional[datetime.date] = Query(None, description="Date before (not including date specified)"),
    channel: Optional[List[Channel]] = Query(None, description="Filter by channel"),
    country: Optional[List[Country]] = Query(None, description="Filter by country"),
    os: Optional[List[Os]] = Query(None, description="Filter by OS"),
    # Paging
    skip: int = 0,
    limit: Optional[int] = None,
    # Other
    db: Session = Depends(get_session),
):
    query = _create_query(db, group_by)
    query = _handle_filtering(query, date_from, date_to, date_after, date_before, channel, country, os)
    query = _handle_sorting(query, sort_by)
    query = _handle_paging(query, skip, limit)

    return query.all()


def _create_query(db, group_by):
    if not group_by:
        cpi = case([(Metric.installs != 0, Metric.spend / Metric.installs)], else_=None)
        return db.query(*inspect(Metric).attrs, cpi.label("cpi"))

    group_args = []

    for param in group_by:
        arg = getattr(Metric, param)
        group_args.append(arg)

    cpi = case([(func.sum(Metric.installs) != 0, func.sum(Metric.spend) / func.sum(Metric.installs))], else_=None)

    query = db.query(
        *group_args,
        func.sum(Metric.impressions).label("impressions"),
        func.sum(Metric.clicks).label("clicks"),
        func.sum(Metric.installs).label("installs"),
        func.sum(Metric.spend).label("spend"),
        func.sum(Metric.revenue).label("revenue"),
        cpi.label("cpi"),
    ).group_by(*group_args)

    return query


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
    if not sort_by:
        return query

    order_args = []

    for param in sort_by:
        is_desc = param.startswith("-")
        attr_name = param.lstrip("-")
        arg = desc(attr_name) if is_desc else asc(attr_name)
        order_args.append(arg)

    query = query.order_by(*order_args)

    return query


def _handle_paging(query, skip, limit):
    return query.offset(skip).limit(limit)
