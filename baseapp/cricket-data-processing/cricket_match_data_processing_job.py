from baseapp.utils.file_utils import FileUtils
from baseapp.utils.config_utils import ConfigUtils
from datetime import datetime
import pandas as pd
import os
import json

def get_ball_by_ball_info(df):
    """

    :param df:
    :return:
    """
    desired_cols = ['info.balls_per_over', 'info.city', 'info.dates', 'info.event.name',
                    'info.event.match_number', 'info.gender', 'info.match_type', 'info.officials.match_referees',
                    'info.officials.tv_umpires', 'info.officials.umpires', 'info.outcome.winner',"info.outcome.by.runs",
                    "info.outcome.by.wickets", 'info.overs', 'info.player_of_match', "innings"]

    if "info.outcome.by.runs" in df.columns:
        df["info.outcome.by.wickets"] = "NA"

    if "info.outcome.by.wickets" in df.columns:
        df["info.outcome.by.runs"] = "NA"

    desired_cols = desired_cols.append("info.match_type_number") if "info.match_type_number" in df.columns else desired_cols
    df = df[desired_cols].copy()
    df = df.explode('innings', ignore_index=True)
    df["team"] = df["innings"].apply(lambda x: x.get("team"))
    df["overs_list"] = df["innings"].apply(lambda x: x.get("overs"))
    df["power_play"] = df["innings"].apply(lambda x: x.get("powerplays"))
    df = df.explode('overs_list', ignore_index=True)
    df["over"] = df["overs_list"].apply(lambda x: x.get("over"))
    df["over"] = df["over"].apply(lambda x: x + 1)
    df["deliveries_list"] = df["overs_list"].apply(lambda x: x.get("deliveries"))
    df = df.explode('deliveries_list', ignore_index=True)
    df["batter"] = df["deliveries_list"].apply(lambda x: x.get("batter"))
    df["bowler"] = df["deliveries_list"].apply(lambda x: x.get("bowler"))
    df["non_striker"] = df["deliveries_list"].apply(lambda x: x.get("non_striker"))
    df["runs"] = df["deliveries_list"].apply(lambda x: x.get("runs"))
    df["wickets"] = df["deliveries_list"].apply(lambda x: x.get("wickets"))
    df["batter_runs"] = df["runs"].apply(lambda x: x.get("batter"))
    df["extra_runs"] = df["runs"].apply(lambda x: x.get("extras"))
    df["total_runs"] = df["runs"].apply(lambda x: x.get("total"))
    df.drop("runs", axis=1, inplace=True)
    df.drop("deliveries_list", axis=1, inplace=True)
    df = df.explode('wickets', ignore_index=True)
    df["wicket_kind"] = df["wickets"].apply(lambda x: None if x is None else x.get("kind"))
    df["wicket_player_out"] = df["wickets"].apply(lambda x: None if x is None else x.get("player_out"))
    df["wicket_fielders"] = df["wickets"].apply(lambda x: None if x is None else x.get("fielders"))
    df.drop("wickets", axis=1, inplace=True)
    df.drop("innings", axis=1, inplace=True)
    df.drop("overs_list", axis=1, inplace=True)
    df["over_ball_no"] = df.groupby(["info.match_type_number", "team", "over"]).cumcount() + 1 if "info.match_type_number" in df.columns else df.groupby(["team", "over"]).cumcount() + 1
    df['over_ball_no_str'] = df['over'].astype(str) + '.' + df['over_ball_no'].astype(str)
    cols = []
    for x in df.columns:
        if "info." in x:
            cols.append(x[5:].replace(".", "_"))
        else:
            cols.append(x)
    df.columns = cols
    return df


def transform_match_info(df_match_info):
    """

    :param df_match_info:
    :return:
    """
    df_match_info.columns = [x[5:].replace(".", "_") for x in df_match_info.columns if "info." in x]
    desired_columns = [x for x in df_match_info.columns if "registry_people" not in x]
    df_match_info = df_match_info[desired_columns].copy()
    prefix = 'players_'
    player_columns = [col for col in df_match_info.columns if col.startswith(prefix)]
    df_match_info['concatenated_players'] = df_match_info[player_columns].apply(lambda x: '_'.join(x.dropna().astype(str)), axis=1)
    df_match_info = df_match_info.drop(columns=player_columns)
    return df_match_info

def get_people_registry(df_match_info):
    """

    :param df_match_info:
    :return:
    """

    def extract_value(row):
        for value in row:
            if pd.notna(value):
                return value

    registry_column_list = list(set([x for x in df_match_info.columns if "info.registry.people" in x]))
    df_people_registry = df_match_info[registry_column_list].copy()
    df_people_registry = df_people_registry.T
    df_people_registry["Id"] = df_people_registry.apply(extract_value, axis=1)
    df_people_registry.reset_index(names=["Name"], inplace=True)
    df_people_registry = df_people_registry[["Id", "Name"]]
    df_people_registry["Name"] = df_people_registry["Name"].apply(lambda x: x.split(".")[-1].strip())
    return df_people_registry

def process_match_files(files_to_process: list, processed_dir_path: str) -> (list, list):
    """

    :param files_to_process:
    :param processed_dir_path:
    :return:
    """
    processed_file_list = []
    unprocessed_file_list = []
    for file_path in files_to_process:
        print(file_path)
        try:
            with open(file_path, 'r') as json_path:
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                data = json.load(json_path)
                df = pd.json_normalize(data)
                info_column_list = [x for x in df.columns if "info." in x]
                df_match_info = df[info_column_list].copy()
                df_people_registry = get_people_registry(df_match_info)
                df_match_info_transformed = transform_match_info(df_match_info)
                df_ball_by_ball_info = get_ball_by_ball_info(df)
                df_ball_by_ball_info.to_csv(os.path.join(*[processed_dir_path, f"ball_by_ball_{file_name}.csv"]), index=False)
                processed_file_list.append(file_path)
        except Exception as e:
            print(f"Exception - {e}")
            unprocessed_file_list.append(file_path)
    return processed_file_list, unprocessed_file_list

if __name__ == '__main__':
    CONFIG_FILE_NAME = "data-processing-config.json"
    config_path = os.path.join(os.getcwd(), CONFIG_FILE_NAME)
    job_config = ConfigUtils.read_json_config(config_path)
    data_dir = job_config.get("data-dir")
    files_to_process = FileUtils.list_files(dir=data_dir, file_extension="json")
    FileUtils.create_dir_if_not_exist(job_config.get("processed-data-dir"))
    processed, unprocessed = process_match_files(files_to_process, job_config.get("processed-data-dir"))
    combine_flag = job_config.get("combine")
    if combine_flag:
        processed_file = FileUtils.list_files(dir=job_config.get("processed-data-dir"), file_extension="csv")
        combined_df_list = []
        for data_file in processed_file:
            df = pd.read_csv(data_file)
            combined_df_list.append(df)
        combined_df_list = pd.concat(combined_df_list)
        combined_df_list.to_csv(f"{datetime.now().strftime('%Y%B%d%H%M%S')}.csv")
    print(unprocessed)

