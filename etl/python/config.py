workspaces = [
    {
        "name": "csc",
        "primary_datasets": ["Muon"],
        "me_startswith": ["CSC/CSCOfflineMonitor/recHits/"],
        "indexer_queue": "indexer-csc",
        "bulk_queue": "bulk-csc",
        "priority_queue": "priority-csc",
    },
    {
        "name": "ecal",
        "primary_datasets": ["ZeroBias"],
        "me_startswith": ["EcalBarrel/", "EcalEndcap/", "Ecal/EventInfo/"],
        "indexer_queue": "indexer-ecal",
        "bulk_queue": "bulk-ecal",
        "priority_queue": "priority-ecal",
    },
    {
        "name": "hcal",
        "primary_datasets": ["ZeroBias"],
        "me_startswith": ["Hcal/DigiTask/"],
        "indexer_queue": "indexer-hcal",
        "bulk_queue": "bulk-hcal",
        "priority_queue": "priority-hcal",
    },
    {
        "name": "jetmet",
        "primary_datasets": ["JetMET"],
        "me_startswith": ["JetMET/Jet/", "JetMET/MET/"],
        "indexer_queue": "indexer-jetmet",
        "bulk_queue": "bulk-jetmet",
        "priority_queue": "priority-jetmet",
    },
    {
        "name": "tracker",
        "primary_datasets": ["ZeroBias"],
        "me_startswith": ["PixelPhase1/", "SiStrip/"],
        "indexer_queue": "indexer-tracker",
        "bulk_queue": "bulk-tracker",
        "priority_queue": "priority-tracker",
    },
]

era_cmp_pattern = "Run202*-PromptReco-*"

priority_era = "2024"

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
