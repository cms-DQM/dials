from ...config import priority_era
from ..file_ingesting.tasks import file_ingesting_pipeline_task


def post_load(workspace: dict, inserted_files: list) -> None:
    for file in inserted_files:
        queue_name = (
            workspace["priority_queue"] if priority_era in file["logical_file_name"] else workspace["bulk_queue"]
        )
        kwargs = {
            "file_id": file["file_id"],
            "dataset_id": file["dataset_id"],
            "workspace_name": workspace["name"],
            "workspace_mes": workspace["me_startswith"],
        }
        file_ingesting_pipeline_task.apply_async(kwargs=kwargs, queue=queue_name)
