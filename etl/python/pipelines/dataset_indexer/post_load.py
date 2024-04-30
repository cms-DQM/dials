from ...config import common_indexer_queue
from ..file_indexer.tasks import file_indexer_pipeline_task


def post_load(workspaces: list, primary_datasets: list) -> None:
    file_indexer_pipeline_task.apply_async(
        kwargs={"workspaces": workspaces, "primary_datasets": primary_datasets}, queue=common_indexer_queue
    )
