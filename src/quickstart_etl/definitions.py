from pathlib import Path

import dagster as dg


@dg.definitions
def defs():
    return dg.load_from_defs_folder(project_root=Path(__file__).parent.parent)
