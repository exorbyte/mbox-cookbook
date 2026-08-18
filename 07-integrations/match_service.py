"""A FastAPI service exposing an M|BOX-backed product search over HTTP."""
from contextlib import asynccontextmanager
from typing import List

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from mbox.indexing import TableIndex
from mbox.recall import TableRecallConfig, TableRecallFieldConfig, TableRecallMode

state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["index"] = TableIndex.load_binary("product_catalog_index.zip")
    state["catalog"] = pd.read_csv("datasets/product_catalog.csv")
    yield
    state.clear()


app = FastAPI(title="M|BOX Match Service", lifespan=lifespan)


class MatchRequest(BaseModel):
    query: str
    max_results: int = 3


class MatchCandidate(BaseModel):
    product_name: str
    score: int


class MatchResponse(BaseModel):
    found: bool
    matches: List[MatchCandidate]


@app.get("/health")
def health():
    return {"status": "ok", "indexed_rows": len(state["catalog"])}


@app.post("/match", response_model=MatchResponse)
def match(request: MatchRequest):
    config = TableRecallConfig(
        fields=[TableRecallFieldConfig(input_column="product_name", indexed_column="product_name",
                                        minimum_quality=0, weight=100, mode=TableRecallMode.APPROX)],
        max_results=request.max_results, min_total_match_value=0, include_field_scores=True
    )
    result = state["index"].match(queries=pd.DataFrame({"product_name": [request.query]}), config=config)

    if len(result) == 0 or result["index_row"].iloc[0] == -1:
        return MatchResponse(found=False, matches=[])

    matches = [
        MatchCandidate(product_name=row["product_name_candidate"], score=int(row["product_name_score"]))
        for _, row in result.iterrows()
    ]
    return MatchResponse(found=True, matches=matches)
