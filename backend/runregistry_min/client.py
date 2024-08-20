import runregistry as rr


class RunRegistry:
    def editable_datasets(self, class_name: str, dataset_name: str, global_state: str):
        datasets = rr.get_datasets(
            filter={
                "and": [
                    {"rr_attributes.class": {"=": class_name}},
                    {"name": {"=": dataset_name}},
                    {"dataset_attributes.global_state": {"=": global_state}},
                ],
                "name": {"and": [{"<>": "online"}]},
                # "dataset_attributes.global_state": {
                #     "and": [{"or": [{"=": "OPEN"}, {"=": "SIGNOFF"}, {"=": "COMPLETED"}]}]
                # },
            },
            ignore_filter_transformation=True,
        )
        return sorted([dt["run_number"] for dt in datasets])
