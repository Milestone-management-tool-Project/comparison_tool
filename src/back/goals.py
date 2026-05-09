from datetime import datetime
import os, json
from .file_operations import create_path

class Goals():
    def __init__(self, goal=None, status=None, limit=None):
         self.year = datetime.now().strftime("%Y")
         self.month = datetime.now().strftime("%m")
         self.json_file = create_path(f"json/{self.year}_{self.month}_goals.jsonl")
         self.goal = goal
         self.goals = {}
         self.status = status
         self.json_date = None
         self.limit = limit
         self.key = None

    def create_project(self):
        import uuid
        self.json_date = datetime.now().strftime("%Y-%m-%d")
        recode_id = str(uuid.uuid4())
        if self.goal == " ":
            return "プロジェクト名が登録されていません。プロジェクト名を設定してください。"
        
        self.goals = {
            "ticket_id": recode_id ,"title": self.goal ,"created_at": self.json_date, 
            "description": {
                "overview":"プロジェクト概要",
                "detail": "プロジェクト詳細情報"
                },
                "limit": self.limit,
                "work_domain": []
                }
        
        if not os.path.exists(create_path('json/')):
            os.mkdir(create_path('json/'))
        try:
            with open(self.json_file, 'a', encoding='utf-8') as f:
                data = json.dumps(self.goals, ensure_ascii=False)
                f.write(data + "\n")
        except Exception as e:
            return f"プロジェクト登録時にエラーが発生-> {e}"
    
    def update(self):
        serch_task = None
        serch_date = None
        update_data = []
        self.json_date = datetime.now().strftime("%Y-%m-%d")

        if self.status.lstrip('-').isdigit():
            self.status = int(self.status)
        # check
        if isinstance(self.status, str):
            print(isinstance(self.status, str))
            print(f"ステータス更新時に文字列({self.status})が送られました")
            return "ステータス更新時に文字列が送られました"
        
        if self.status > 1 or self.status < -1:
            print("ステータス更新時に不正な値が送られました")
            return "ステータス更新時に不正な値が送られました"
        
        # update
        if not os.path.exists(self.json_file):
            return "ファイルが作成されていません。タスクを登録してから実行してください。"
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            for data in f.readlines():
                try:
                    file_data = json.loads(data)
                except:
                    return "jsonファイルが見つかりません"
                
                if not isinstance(file_data['status'], int) or file_data['status'] > 1 or file_data['status'] < -1:
                        print( "不正な値を検知")
                        continue
                
                if file_data['status'] == 1:
                    print("既に完了済みのタスクです")
                    continue

                if file_data['status'] == -1 or file_data['status'] == 0:
                    update_data.append(file_data)

        target = []
        for i in update_data:
            if not i['key'] == self.key:
                continue
            target.append(i)

        if not target: return
        
        serch_task = target[0]
        serch_date = self.json_date

        val_a = self.status

        for i in update_data:
            if i['key'] == serch_task['key']:
                i['status'] = val_a
                if val_a == 1:
                    i['updated_at'] = serch_date

        entry_data = []
        with open(self.json_file, 'r', encoding='utf-8')as f:
            for data in f.readlines():
                try:
                    datas = json.loads(data)
                    entry_data.append(datas)
                except:
                    continue
        
        with open(self.json_file, 'w') as f:
            for row in entry_data:
                if row['key'] == serch_task['key']:
                    row = serch_task
                    row['limit'] = self.limit
                    row['updated_at'] = self.json_date
                new_data = json.dumps(row, ensure_ascii=False)
                f.write(new_data + '\n')