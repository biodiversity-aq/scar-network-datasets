import requests
import logging

logger = logging.getLogger(__name__)
session = requests.Session()
session.headers.update({"User-Agent": "biodiversity-aq/scar-network-datasets"})


def get_paged_results(url, limit=100):
    results = list()
    params = dict(
        offset=0,
        limit=limit
    )
    while True:
        res = session.get(url=url, params=params)
        data = res.json()
        if not data["results"]:
            break
        results.extend(data["results"])
        params["offset"] = params["offset"] + params["limit"]
    return results


def get_scar_network_datasets():
    logger.info("Fetching SCAR network datasets")
    datasets = get_paged_results("https://api.gbif.org/v1/network/8534dd20-c368-4a1f-bdaf-e6b390710f89/constituents")
    return datasets


def create_gbif_url(dataset_id):
    return f"https://www.gbif.org/dataset/{dataset_id}"
