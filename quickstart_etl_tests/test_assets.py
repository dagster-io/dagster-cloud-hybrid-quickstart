import dagster as dg
from pathlib import Path


def test_def_can_load():
    defs = dg.ComponentTree.for_project(Path(__file__).parent).build_defs()
    assert defs.resolve_job_def("all_assets_job")