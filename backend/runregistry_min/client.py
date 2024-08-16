import runregistry as rr


class RunRegistry:
    def get_open_runs(self, class_name: str, dataset_name: str):
        datasets = rr.get_datasets(
            filter={
                "and": [
                    {"rr_attributes.class": {"=": class_name}},
                    {"name": {"=": dataset_name}},
                    {"dataset_attributes.global_state": {"=": "OPEN"}},
                ],
                "name": {"and": [{"<>": "online"}]},
                "dataset_attributes.global_state": {
                    "and": [{"or": [{"=": "OPEN"}, {"=": "SIGNOFF"}, {"=": "COMPLETED"}]}]
                },
            },
            ignore_filter_transformation=True,
        )
        return sorted([dt["run_number"] for dt in datasets])
