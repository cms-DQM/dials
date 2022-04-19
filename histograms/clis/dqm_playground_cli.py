import click
import glob
import pandas as pd

PATH = "/eos/project/c/cmsml4dc/ML_2020/PerRun_UL2018_Data/"
FILE_EXAMPLE = "ZeroBias_315257_UL2018.csv"


def get_runs():
    run_files = glob.glob(PATH + "ZeroBias*")
    run_numbers = [x.split("/")[-1].split("_")[1] for x in run_files]
    print(run_numbers)
    return


def get_variables(run_number, subsystem, workspace):
    df = pd.read_csv(PATH + f"ZeroBias_{315257}_UL2018.csv")
    df_variables = df[df["path"].apply(lambda x: subsystem in x)]
    df_variables = df_variables[df_variables["path"].apply(lambda x: workspace in x)]
    variables = df_variables["path"].tolist()
    for variable in variables:
        print(f"    {variable}")
    return


@click.command()
@click.option("--run_list", default=False, help="Provides list of runs.")
@click.option("--variable_list", default=False, help="Provides list of variables.")
@click.option("--run_number", default=0, help="Run number for variable exploration.")
@click.option("--subsystem", default="", help="Subsystem for variable exploration.")
@click.option("--workspace", default="", help="Workspace for variable exploration.")
def cli(run_list, variable_list, run_number, subsystem, workspace):
    """Simple program that provides list of runs / list of variables"""
    if run_list:
        print("List of runs available")
        get_runs()
    elif variable_list:
        # check that run exists
        print(f"Exploring variables available in run {run_number}.")
        print(f"Subsystem: {subsystem}")
        print(f"Workspace: {workspace}")
        # open file and load variables
        print("List of variables")
        get_variables(run_number, subsystem, workspace)
    else:
        return
