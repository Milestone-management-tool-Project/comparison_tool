from datetime import datetime
import os, json
from .file_operations import create_path
import uuid

class Goals():
    def __init__(
            self, goal=None, key=None, domain_key=None,status=0, limit=None, overview=None, datail=None,
            purpose=None, work_domain=None, task_id=None, task_name=None):
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
         self.task_id = task_id
         self.flag = False
         self.task_name = task_name

    def create_project(self):
        recode_id = str(uuid.uuid4())
        self.json_date = datetime.now().strftime("%Y-%m-%d")
        if self.goal == " ":
            return "プロジェクト名が登録されていません。プロジェクト名を設定してください。"
        
        self.goals = {
            "ticket_id": recode_id ,
            "title": self.goal ,
            "created_at": self.json_date, 
            "description": [{"overview": self.overview,"datail": self.datail}],
            "limit": self.limit,
            "completion_flag": self.flag,
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
        if self.label[0]['purpose'] is None or self.label[0]['purpose'] == " ":
            return "目標が登録されていません。"
        if self.label[0]['work_domain'] is None or self.label[0]['work_domain'] == " ":
            return "作業領域が登録されていません。"
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
                        "status": self.status, 
                        "limit": self.limit,
                        "completion_flag": self.flag,
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
        if self.task_id == " ":
            return "タスクが登録されていません。"
        if isinstance(self.status, str):
            return f"statusで文字列が渡されています。-> {self.status}"
        if self.status >= 1 or self.status <= -2:
            return f"statusに不正な値が格納されています。-> {self.status}"
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            datas = [json.loads(line) for line in f.readlines()]
        for i in datas:
            if i['ticket_id'] == self.key:
                for j in i['work_domain']:
                    if j['domain_id'] == self.domain_key:
                        j['task'].append({
                                "task_id": str(id),
                                "title": self.task_name,
                                "created_at": times,
                                "limit": self.limit,
                                "status": self.status,
                                "updated_at": times
                            })
                    else: continue
        with open(self.json_file, 'w', encoding='utf-8') as f :
            for i in datas: 
                f.write(json.dumps(i, ensure_ascii=False) + '\n')
        return datas[0]
        
    def update_status(self):
        time = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                datas = [json.loads(line) for line in f.readlines()]
            for d in datas:
                for i in d['work_domain']:
                    if i['domain_id'] == self.domain_key:
                        for j in i['task']:
                            print(j)
                            if self.task_id == j['task_id']:
                                if isinstance(j['status'], str):
                                    return f"statusに文字列が格納されています。-> {j['status']}"
                                if j['status'] >= 1 or j['status'] <= -2:
                                    return f"statusに不正な値が格納されています。-> {j['status']}"
                                if j['status'] <= 0:
                                    j['status'] = self.status
                                else:
                                    continue
                                if not self.limit is None:
                                    j['limit'] = self.limit
                                else:
                                    continue
                                j['updated_at'] = time
            with open(self.json_file, 'w', encoding='utf-8') as f :
                for i in datas: 
                    f.write(json.dumps(i, ensure_ascii=False) + '\n')
            return datas[0]
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"データの更新時にエラー発生-> {e}"

   # def test_changed_flag(self):
        flag_data = []
        for i in data['work_domain']:
            flag_data = [j['status'] == 1 for j in i['task']]
        result = all(flag_data)
        if result:
            data["work_domain"][0]['completion_flag'] = True
        else:
            data["work_domain"][0]['completion_flag'] = False
        print(data['work_domain'][0]['task'][0])
        print(data['work_domain'][0]['task'][1])
        print(data["work_domain"][0]['completion_flag'])


