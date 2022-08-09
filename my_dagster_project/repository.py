from dagster import load_assets_from_package_module, repository, define_asset_job

from my_dagster_project import assets


@repository
def my_dagster_project():
    return [
        load_assets_from_package_module(assets),
        define_asset_job(name="all_assets_job"),
    ]
