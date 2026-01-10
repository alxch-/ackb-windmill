# py313

import os
import httpx
import wmill
from typing import Optional, Dict, Any, Set

USE_SANDBOX = False
PAGE_SIZE = 50
MAX_PAGES = 20

def _base_url(use_sandbox: bool) -> str:
    return "https://sandbox-api.piste.gouv.fr/cassation/judilibre/v1.0" if use_sandbox \
           else "https://api.piste.gouv.fr/cassation/judilibre/v1.0"

def _headers(key_id: str) -> Dict[str, str]:
    # Per Judilibre README, KeyId header is required
    return {"accept": "application/json", "KeyId": key_id}

def _extract_id(result: Dict[str, Any]) -> Optional[str]:
    # Be tolerant to schema nuances
    return (
        result.get("id")
        or result.get("_id")
        or (result.get("decision") or {}).get("id")
        or (result.get("source") or {}).get("id")
    )

def main(queries: list = [],) -> list[str]:
    url = f"{_base_url(USE_SANDBOX)}/search"
    seen_ids = set()
    for q in queries:
        print(f"Starting decision check for query {q}")
        with httpx.Client(headers=_headers(wmill.get_variable("u/alex/piste_api_prod")), timeout=30.0) as client:
            for page in range(0, MAX_PAGES):
                params = {"query": q, "page_size": PAGE_SIZE, "page": page, "jurisdiction": "tj", "operator": "and"}
                resp = client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                results = data.get("results", [])
                if not results:
                    break

                for result in results:
                    did = _extract_id(result)
                    if not did:
                        continue
                    if did not in seen_ids:
                        seen_ids.add(did)
    current_state =  set(wmill.get_state()) if wmill.get_state() else set()
    new_items = seen_ids - current_state
    new_state = current_state.union(seen_ids)
    wmill.set_state(list(new_state))
    return list(new_items)

