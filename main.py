from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI

from constants import DATA_PORTAL_AGGREGATIONS

app = FastAPI()
es = AsyncElasticsearch(["localhost:9200"])


@app.get("/{index}")
async def root(index: str, offset: int = 0, limit: int = 15,
               sort: str = "rank:desc", filter: str | None = None):
    body = dict()
    body["aggs"] = dict()
    for aggregation_field in DATA_PORTAL_AGGREGATIONS:
        body["aggs"][aggregation_field] = {
            "terms": {"field": aggregation_field}
        }
    if filter:
        filters = filter.split(",")
        body["query"] = {"bool": {"filter": []}}
        for filter_item in filters:
            filter_name, filter_value = filter_item.split(":")
            body["query"]["bool"]["filter"].append(
                {"term": {filter_name: filter_value}}
            )
    response = await es.search(
        index=index, sort=sort, from_=offset, size=limit, body=body
    )
    data = dict()
    data['count'] = response['hits']['total']['value']
    data['results'] = response['hits']['hits']
    data['aggregations'] = response['aggregations']
    return data


@app.get("/{index}/{record_id}")
async def details(index: str, record_id: str):
    data = dict()
    data['index'] = index
    data['record_id'] = record_id
    return data
