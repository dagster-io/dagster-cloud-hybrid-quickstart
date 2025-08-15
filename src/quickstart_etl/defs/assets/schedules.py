import dagster as dg


@dg.definitions
def defs():
    return dg.Definitions(
        schedules=[
            dg.ScheduleDefinition(
                job=dg.define_asset_job(name="all_assets_job"),
                cron_schedule="0 0 * * *",
            )
        ]
    )