import dlt
from dagster import AssetExecutionContext, SourceAsset, AssetKey
from dlt.sources.helpers import requests
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets, DagsterDltTranslator
from typing import Iterable

dlt_resource = DagsterDltResource()

@dlt.source
def ebirdapi_source(loc_code: str = 'US-WA', api_secret_key=dlt.secrets.value):
    return (
        recent_observations(loc_code, api_secret_key),
        taxonomy(api_secret_key),
        taxa_local_codes(api_secret_key),
        taxonomy_versions(api_secret_key)
    )

def _create_auth_headers(api_secret_key):
    """Constructs Bearer type authorization header which is the most common authorization method"""
    headers = {"X-eBirdApiToken": f"{api_secret_key}"}
    return headers

@dlt.resource(write_disposition="replace")
def recent_observations(loc_code: str, api_secret_key=dlt.secrets.value):
    headers = _create_auth_headers(api_secret_key)

    ebird_api_url = f'https://api.ebird.org/v2/data/obs/{loc_code}/recent/notable?detail=full'

    response = requests.get(ebird_api_url, headers=headers) #, params=params
    response.raise_for_status()
    data = response.json()
    yield data

@dlt.resource(write_disposition="replace")
def taxonomy(api_secret_key=dlt.secrets.value):
    headers = _create_auth_headers(api_secret_key)

    ebird_api_url = 'https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json'

    response = requests.get(ebird_api_url, headers=headers) #, params=params
    response.raise_for_status()
    data = response.json()
    yield data

@dlt.resource(write_disposition="replace")
def taxa_local_codes(api_secret_key=dlt.secrets.value):
    headers = _create_auth_headers(api_secret_key)

    ebird_api_url = 'https://api.ebird.org/v2/ref/taxa-locales/ebird'

    response = requests.get(ebird_api_url, headers=headers) #, params=params
    response.raise_for_status()
    data = response.json()
    yield data

@dlt.resource(write_disposition="replace")
def taxonomy_versions(api_secret_key=dlt.secrets.value):
    headers = _create_auth_headers(api_secret_key)

    ebird_api_url = 'https://api.ebird.org/v2/ref/taxonomy/versions'

    response = requests.get(ebird_api_url, headers=headers) #, params=params
    response.raise_for_status()
    data = response.json()
    yield data

ebird_api = ebirdapi_source()

ebird_upstream_asset = SourceAsset(key="ebird_api")

class EbirdDagsterDltTranslator(DagsterDltTranslator):
    def get_deps_asset_keys(self, resource: DagsterDltResource) -> Iterable[AssetKey]:
        return [AssetKey("ebird_api")]

@dlt_assets(
    dlt_source=ebird_api,
    dlt_pipeline=dlt.pipeline(
        pipeline_name='ebirdapi',
        destination='duckdb',
        # staging='filesystem',
        dataset_name='ebirdapi_data',
        import_schema_path="schemas/import",
        export_schema_path="schemas/export",
        # full_refresh=True,
        progress="log",
    ),
    name="ebird_api",
    dlt_dagster_translator=EbirdDagsterDltTranslator(),
)
def dagster_ebirdapi_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
