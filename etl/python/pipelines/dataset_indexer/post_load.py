from ..file_indexer.tasks import file_indexer_pipeline_task


def post_load(workspace: dict) -> None:
    file_indexer_pipeline_task.apply_async(kwargs={"workspace": workspace}, queue=workspace["indexer_queue"])
