# List of open items per app

## General

- Check conflict between unicity and bulk creation. Currently using "ignore_conflicts=True", not sure about the impact. Worth checking transaction.atomic and other options.
- Define proper way of handling unicity of Campaign (Online / Prompt / ReReco / UL) and Dataset (ZeroBias / SingleMu / )
- Add tests!
- Add config file with list of [MonitorElement](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PerLsDQMIO#What_are_DQMIO_per_LS_data) and [runs](https://twiki.cern.ch/twiki/bin/view/CMS/ML4TrkDQM#Reference_runs_Intervals_of_Vali) corresponding to changes in calibration / settings

## Development

### [Template] App

__Model__

- add fields / update type / add constraints
- ...

__Management__

- add options to upload information
- create config files to increase modularity and cope with other subsystems
- ...

__View__

- move from Semantic UI to Bootstrap
- create option
- ...

### Runs

__Model__

- add information from OMS
- add flags

### Run histos

__Management__

- load list of histograms to be saved to database from config file

### Run certification

