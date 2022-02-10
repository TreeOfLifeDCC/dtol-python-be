from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI

from constants import DATA_PORTAL_AGGREGATIONS

app = FastAPI()
es = AsyncElasticsearch(["localhost:9200"])


@app.get("/{index}")
async def root(index: str, offset: int = 0, limit: int = 15,
               sort: str = "rank:desc"):
    body = dict()
    body["aggs"] = dict()
    for aggregation_field in DATA_PORTAL_AGGREGATIONS:
        body["aggs"][aggregation_field] = {"terms": {"field": aggregation_field}}
    response = await es.search(
        index=index, sort=sort, from_=offset, size=limit, body=body
    )
    data = dict()
    data['count'] = response['hits']['total']['value']
    data['results'] = response['hits']['hits']
    data['aggregations'] = response['aggregations']
    return data
