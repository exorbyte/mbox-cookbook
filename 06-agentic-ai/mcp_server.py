"""An MCP server exposing an M|BOX-backed product search as a single standard tool.

MCP over stdio uses stdout exclusively for JSON-RPC protocol messages, so anything
else written to it corrupts the transport. M|BOX itself logs a license line and a
startup banner as soon as it's imported, so we redirect stdout to the null device
for the import and index build to keep those off the wire. This catches the
synchronous log line reliably; see the notebook for a caveat on the rest.
"""
import os
import time

_stdout_fd = os.dup(1)
_devnull_fd = os.open(os.devnull, os.O_WRONLY)
os.dup2(_devnull_fd, 1)
try:
    import pandas as pd
    from mbox.indexing import TableIndexer
    from mbox.recall import TableRecallConfig, TableRecallFieldConfig, TableRecallMode

    catalog = pd.read_csv("datasets/product_catalog.csv")
    index = TableIndexer.create_index(
        catalog, index_columns=["product_name", "description", "unit_price"], tmp_dir="tmp_index_mcp"
    )
    time.sleep(2)
finally:
    os.dup2(_stdout_fd, 1)
    os.close(_stdout_fd)
    os.close(_devnull_fd)

from mcp.server import MCPServer

server = MCPServer("mbox-catalog")


def _text_only_match(product_name: str, max_results: int) -> pd.DataFrame:
    config = TableRecallConfig(
        fields=[TableRecallFieldConfig(input_column="product_name", indexed_column="product_name",
                                        minimum_quality=0, weight=100, mode=TableRecallMode.APPROX)],
        max_results=max_results, min_total_match_value=0, include_field_scores=True
    )
    return index.match(queries=pd.DataFrame({"product_name": [product_name]}), config=config)


@server.tool()
def search_products(product_name: str, max_price: float | None = None, max_results: int = 3) -> dict:
    """Search the product catalog by name, tolerating typos, optionally constrained by a maximum price."""
    if max_price is None:
        r = _text_only_match(product_name, max_results)
        if len(r) == 0 or r["index_row"].iloc[0] == -1:
            return {"found": False, "matches": []}
        matches = [{"product_name": row["product_name_candidate"],
                    "match_confidence": int(row["product_name_score"]),
                    "overall_score": int(row["overall_score"])} for _, row in r.iterrows()]
        return {"found": True, "matches": matches}

    fields = [
        TableRecallFieldConfig(input_column="product_name", indexed_column="product_name",
                                minimum_quality=0, weight=70, mode=TableRecallMode.APPROX),
        TableRecallFieldConfig(input_column="unit_price", indexed_column="unit_price",
                                minimum_quality=0, weight=30, mode=TableRecallMode.NUM_LOWER)
    ]
    config = TableRecallConfig(fields=fields, max_results=max_results, min_total_match_value=0, include_field_scores=True)
    r = index.match(queries=pd.DataFrame({"product_name": [product_name], "unit_price": [max_price]}), config=config)

    if len(r) > 0 and r["index_row"].iloc[0] != -1:
        matches = [{"product_name": row["product_name_candidate"],
                    "match_confidence": int(row["product_name_score"]),
                    "overall_score": int(row["overall_score"])} for _, row in r.iterrows()]
        return {"found": True, "matches": matches}

    unconstrained = _text_only_match(product_name, max_results=1)
    if len(unconstrained) > 0 and unconstrained["index_row"].iloc[0] != -1:
        row = unconstrained.iloc[0]
        actual_price = catalog.loc[catalog["product_name"] == row["product_name_candidate"], "unit_price"].iloc[0]
        return {
            "found": False,
            "matches": [],
            "note": "A matching product exists but exceeds the requested max_price.",
            "closest_match": {
                "product_name": row["product_name_candidate"],
                "match_confidence": int(row["product_name_score"]),
                "actual_price": float(actual_price)
            }
        }

    return {"found": False, "matches": []}


if __name__ == "__main__":
    server.run()
