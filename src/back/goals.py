from datetime import datetime
import os, json
from .file_operations import create_path
import uuid

class Goals():
    def __init__(
            self, goal=None, key=None, domain_key=None,status=None, limit=None, overview=None, datail=None,
            purpose=None, work_domain=None, task=None):
         self.year = datetime.now().strftime("%Y")
         self.month = datetime.now().strftime("%m")
         self.json_file = create_path(f"json/{self.year}_{self.month}_goals.jsonl")
         self.goal = goal
         self.goals = {}
         self.status = status
         self.json_date = None
         self.limit = limit
         self.key = key
         self.label = [{"purpose": purpose,"work_domain": work_domain}]
         self.domain_key = domain_key
         self.overview = overview
         self.datail = datail
         self.task = task

         print(self.datail, self.overview)
    def create_project(self):
        self.json_date = datetime.now().strftime("%Y-%m-%d")
        recode_id = str(uuid.uuid4())
        if self.goal == " ":
            return "プロジェクト名が登録されていません。プロジェクト名を設定してください。"
        
        self.goals = {
            "ticket_id": recode_id ,"title": self.goal ,"created_at": self.json_date, 
            "description": [{"overview": self.overview,"datail": self.datail}],
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
    
    def create_child_ticket(self):
        id = uuid.uuid4()

        times = datetime.now().strftime('%H:%M:%S')
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                datas = [json.loads(line) for line in f.readlines()]
            for i in datas:
                if i['ticket_id'] == self.key:
                    i['work_domain'].append({
                        "domain_id": str(id),
                        "label": self.label,
                        "overview": self.overview,
                        "created_at": times,
                        "states": 0, 
                        "limit": '2026-05-11',
                        "completion_flag": True,
                        "task":[]
                    })
            with open(self.json_file, 'w', encoding='utf-8') as f :
                for i in datas:
                    f.write(json.dumps(i, ensure_ascii=False) + '\n')
            return datas[0]
        
        except Exception as e:
            return f"保存時に問題が発生{e}"
        
    def create_grandchild_ticket(self):
        id = uuid.uuid4()
        times = datetime.now().strftime('%H:%M:%S')

        with open(self.json_file, 'r', encoding='utf-8') as f:
            datas = [json.loads(line) for line in f.readlines()]
        for i in datas:
            if i['ticket_id'] == self.key:
                for j in i['work_domain']:
                    if j['domain_id'] == self.domain_key:
                        j['task'].append({
                                "task_id": str(id),
                                "title": self.task,
                                "created_at": times,
                                "limit": self.limit,
                                "states": self.status,
                                "completion_flag": False,
                                "updated_at": times
                            })
                    else: continue
        with open(self.json_file, 'w', encoding='utf-8') as f :
            for i in datas: 
                f.write(json.dumps(i, ensure_ascii=False) + '\n')
        return datas[0]