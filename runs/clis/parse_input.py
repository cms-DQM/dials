import click

PATH='/eos/project/c/cmsml4dc/ML_2020/PerRun_UL2018_Data/'
FILE_EXAMPLE='ZeroBias_315257_UL2018.csv'

@click.command()
@click.option('--run_list', default=False, help='Provides list of runs.')
@click.option('--variable_list', default=False, help='Provides list of variables.')


def get_runs_and_variables(run_list, variable_list):
    """Simple program that provides list of runs / list of variables"""
    if run_list == True:
        print('Here is the list of runs available')
    elif variable_list == True:
        print('Here is the list of variables')
    else:
        return


if __name__ == '__main__':
    get_runs_and_variables()

