from baseapp.utils.file_utils import FileUtils
from baseapp.utils.config_utils import ConfigUtils
import pandas as pd
import os
import json

def get_ball_by_ball_info(df):
    df = df[["info.match_type", "info.match_type_number", "innings"]]
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
    df["over_ball_no"] = df.groupby(["info.match_type_number", "team", "over"]).cumcount() + 1
    df['over_ball_no_str'] = df['over'].astype(str) + '.' + df['over_ball_no'].astype(str)
    return df


def transform_match_info(df_match_info):
    df_match_info.columns = [x[5:].replace(".", "_") for x in df_match_info.columns if "info." in x]
    desired_columns = [x for x in df_match_info.columns if "registry_people" not in x]
    df_match_info = df_match_info[desired_columns].copy()
    prefix = 'players_'
    player_columns = [col for col in df_match_info.columns if col.startswith(prefix)]
    df_match_info['concatenated_players'] = df_match_info[player_columns].apply(lambda x: '_'.join(x.dropna().astype(str)), axis=1)
    df_match_info = df_match_info.drop(columns=player_columns)
    return df_match_info

def get_people_registry(df_match_info):

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

def process_match_files(files_to_process: list) -> (list, list):
    processed_file_list = []
    unprocessed_file_list = []
    for file_path in files_to_process[:3]:
        try:
            with open(file_path, 'r') as json_path:
                print(file_path)
                data = json.load(json_path)
                df = pd.json_normalize(data)
                info_column_list = [x for x in df.columns if "info." in x]
                df_match_info = df[info_column_list].copy()
                df_people_registry = get_people_registry(df_match_info)
                df_match_info_transformed = transform_match_info(df_match_info)
                df_ball_by_ball_info = get_ball_by_ball_info(df)
                processed_file_list.append(file_path)
        except Exception as e:
            print(e)
            unprocessed_file_list.append(file_path)
    return processed_file_list, unprocessed_file_list

if __name__ == '__main__':
    CONFIG_FILE_NAME = "data-processing-config.json"
    config_path = os.path.join(os.getcwd(), CONFIG_FILE_NAME)
    job_config = ConfigUtils.read_json_config(config_path)
    odi_data_dir = job_config.get("odi-data-dir")
    odi_files_to_process = FileUtils.list_files(dir=odi_data_dir, file_extension="json")
    FileUtils.create_dir_if_not_exist(job_config.get("odi-processed-data-dir"))
    process_match_files(odi_files_to_process)
