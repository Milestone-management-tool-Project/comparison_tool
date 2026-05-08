import csv, json
from datetime import datetime
import pathlib
import os
import platform

def create_path(file):
    target_dir = 'milestone_manager/'
    # os judgement
    if platform.system() == 'Linux':
        base_path = os.path.join(pathlib.Path.home(), '.local/share/')
    if platform.system() == 'Windows':
        env = os.environ.get('APPDATA')
        base_path = pathlib.Path(env)
    if platform.system() == 'Darwin':
        base_path = os.path.join(pathlib.Path.home(), 'Library/Application Support/')


    if not os.path.exists(os.path.join(base_path, target_dir)):
        os.mkdir(os.path.join(base_path, target_dir))
    file_path = pathlib.Path(os.path.join(base_path, os.path.join(target_dir, file)))

    return file_path


class FileSearch:
    def __init__(self, month, year):
        self.month = month
        self.year = year

    def reard_to_jsonl(self):
        return_data = []
        json_file = create_path(f"json/{self.year}_{self.month}_goals.jsonl")
        if not os.path.exists(json_file):
            return "ファイルが見つかりません。"
        
        with open(json_file, 'r', encoding='utf-8') as f:
            for data in f.readlines():
                try:
                    file_data = json.loads(data)
                    return_data.append(file_data)
                except:
                    return "jsonファイルが見つかりません"
        return return_data
    
    def reard_to_csv(self):
        csv_file = create_path(f"csv/time_{self.year}-{self.month}.csv")
        return_data = []
        print(csv_file)
        if not os.path.exists(csv_file):
            return "ファイルが見つかりません"
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            try:
                writer = csv.reader(f)
                for data in writer:
                    return_data.append(data)
                return return_data
            except Exception as e:
                return f"ファイル検索時に問題が発生-> {e}"