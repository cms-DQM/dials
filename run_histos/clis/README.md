# Simple Command Line Interface to explore runs

Developed using [Click](https://click.palletsprojects.com/en/8.0.x/).

To build the cli:
```
pip3 install --editable .
```

To run the cli:
```
dqm_playground_cli --help
Usage: dqm_playground_cli [OPTIONS]

  Simple program that provides list of runs / list of variables

Options:
  --run_list BOOLEAN       Provides list of runs.
  --variable_list BOOLEAN  Provides list of variables.
  --run_number INTEGER     Run number for variable exploration.
  --subsystem TEXT         Subsystem for variable exploration.
  --workspace_str TEXT     Workspace string for variable exploration.
  --help                   Show this message and exit.
```

Accessing all available runs:
```
dqm_playground_cli --run_list=True
```

Accessing all variables from a given run (315257):
```
dqm_playground_cli --variable_list=True --run_number=315257
```

Restricting to a given subsystem (Tracking):
```
dqm_playground_cli --variable_list=True --run_number=315257 --subsystem=Tracking
```

Restricting to a given (sub-)workspace:
```
dqm_playground_cli --variable_list=True --run_number=315257 --subsystem=Tracking --workspace=GeneralProperties/Chi2_GenTk
```
