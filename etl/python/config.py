workspaces = [
    {
        "name": "csc",
        "primary_datasets": ["Muon"],
        "me_startswith": ["CSC/CSCOfflineMonitor/recHits/"],
        "indexer_queue": "csc-indexer",
        "bulk_queue": "csc-bulk",
        "priority_queue": "csc-priority",
    },
    {
        "name": "ecal",
        "primary_datasets": ["ZeroBias"],
        "me_startswith": ["EcalBarrel/", "EcalEndcap/", "Ecal/EventInfo/"],
        "indexer_queue": "ecal-indexer",
        "bulk_queue": "ecal-bulk",
        "priority_queue": "ecal-priority",
    },
    {
        "name": "hcal",
        "primary_datasets": ["ZeroBias"],
        "me_startswith": ["Hcal/DigiTask/"],
        "indexer_queue": "hcal-indexer",
        "bulk_queue": "hcal-bulk",
        "priority_queue": "hcal-priority",
    },
    {
        "name": "jetmet",
        "primary_datasets": ["JetMET"],
        "me_startswith": ["JetMET/Jet/", "JetMET/MET/"],
        "indexer_queue": "jetmet-indexer",
        "bulk_queue": "jetmet-bulk",
        "priority_queue": "jetmet-priority",
    },
    {
        "name": "tracker",
        "primary_datasets": ["ZeroBias"],
        "me_startswith": ["PixelPhase1/", "SiStrip/"],
        "indexer_queue": "tracker-indexer",
        "bulk_queue": "tracker-bulk",
        "priority_queue": "tracker-priority",
    },
]

era_cmp_pattern = "Run202*"

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
