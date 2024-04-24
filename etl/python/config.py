workspaces = [
    {
        "name": "csc",
        "primary_datasets": ["Muon", "StreamExpress"],
        "me_startswith": ["CSC/CSCOfflineMonitor/recHits/"],
        "bulk_queue": "csc-bulk",
        "priority_queue": "csc-priority",
    },
    {
        "name": "ecal",
        "primary_datasets": ["ZeroBias"],
        "me_startswith": ["EcalBarrel/", "EcalEndcap/", "Ecal/EventInfo/"],
        "bulk_queue": "ecal-bulk",
        "priority_queue": "ecal-priority",
    },
    {
        "name": "hcal",
        "primary_datasets": ["ZeroBias"],
        "me_startswith": ["Hcal/DigiTask/"],
        "bulk_queue": "hcal-bulk",
        "priority_queue": "hcal-priority",
    },
    {
        "name": "jetmet",
        "primary_datasets": ["JetMET"],
        "me_startswith": ["JetMET/Jet/", "JetMET/MET/"],
        "bulk_queue": "jetmet-bulk",
        "priority_queue": "jetmet-priority",
    },
    {
        "name": "tracker",
        "primary_datasets": [
            "ZeroBias",
            "StreamExpress",
            "HIForward0",
            "HIPhysicsRawPrime0",
            "StreamHIExpressRawPrime",
        ],
        "me_startswith": ["PixelPhase1/", "SiStrip/"],
        "bulk_queue": "tracker-bulk",
        "priority_queue": "tracker-priority",
    },
]

primary_datasets = [elem for ws in workspaces for elem in ws["primary_datasets"]]
primary_datasets = sorted(set(primary_datasets))

pds_queues = {
    primary_dataset: {
        "bulk_queue": f"{primary_dataset}-downloader-bulk",
        "priority_queue": f"{primary_dataset}-downloader-priority",
    }
    for primary_dataset in primary_datasets
}

era_cmp_pattern = "*Run202*"

priority_era = "Run2024"

th1_types = (
    3,
    4,
    5,
)

th2_types = (
    6,
    7,
    8,
)

dev_env_label = "dev"

common_chunk_size = 5000
th2_chunk_size = 1000  # carefully chosen to use little memory but keep high inserting speed

common_indexer_queue = "common-indexer"
