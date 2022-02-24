import click

PATH='/eos/project/c/cmsml4dc/ML_2020/PerRun_UL2018_Data/'
FILE_EXAMPLE='ZeroBias_315257_UL2018.csv'

@click.command()
@click.option('--run_list', default=False, help='Provides list of runs.')
@click.option('--variable_list', default=False, help='Provides list of variables.')
@click.option('--run_number', default=0, help='Run number for variable exploration.')
@click.option('--subsystem', default='Tracking', help='Subsystem for variable exploration.')
@click.option('--workspace_str', default='', help='Workspace string for variable exploration.')
def cli(run_list, variable_list, run_number, subsystem, workspace_str):
    """Simple program that provides list of runs / list of variables"""
    if run_list == True:
        print('List of runs available')
    elif variable_list == True:
        # check that run exists
        print(f'Exploring variables available in run {run_number}.')
        print(f'Subsystem: {subsystem}')
        print(f'Workspace: {workspace_str}')
        # open file and load variables
        print('List of variables')
    else:
        return

