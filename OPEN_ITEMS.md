# List of open items per app

## General

- Check conflict between unicity and bulk creation. Currently using "ignore_conflicts=True", not sure about the impact. Worth checking transaction.atomic and other options.
- Define proper way of handling unicity of Campaign (Online / Prompt / ReReco / UL) and Dataset (ZeroBias / SingleMu / )

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

__Test__

- add test for item

### Runs

__Model__

- add information from OMS

__View__

- create default views for runs/ & run/<int>

__Test__

- Add tests for views, check views display when empty DB

### Run histos

__Management__

- load list of histograms to be saved to database from config file

### Run certification

