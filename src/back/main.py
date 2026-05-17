import fastapi
import fastapi.middleware.cors
import src.back.goals as goals, src.back.times as times
import src.back.file_operations as files
from typing import Annotated, List, Dict

app = fastapi.FastAPI()
timer = times.TimeCheker()

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["http://localhost:5173"]
)

@app.get("/timer/start")
def timer_start():
    result = timer.start_checker()
    return result

@app.post("/timer/stop")
def timer_end():
    result = timer.end_checker()
    return result

@app.get("/timer/today")
def today_timer():
    result = timer.import_to_csv()
    return result

@app.post("/goals/create_project")
def goals_set(ticket, limit, overview, datail):
    result = goals.Goals(goal=ticket, limit=limit, overview=overview, datail=datail).create_project()
    return result

@app.post("/goals/create_child_ticket")
def create_child_ticket(project_key, limit, overview, purpose, work_domain):
    result = goals.Goals(key=project_key, limit=limit,overview=overview , purpose=purpose, work_domain=work_domain).create_child_ticket()
    return result

@app.post("/goals/create_grandchild_ticket")
def create_grandchild_ticket(project_key, status:int, limit, domain_key, task_name):
    result = goals.Goals(key=project_key, domain_key=domain_key ,status=status, limit=limit, task_name=task_name).create_grandchild_ticket()
    return result

@app.post("/goals/update_grandchild_ticket")
def create_grandchild_ticket(project_key, status:int, limit, domain_key, task_id):
    result = goals.Goals(key=project_key, domain_key=domain_key ,status=status, limit=limit, task_id=task_id).update_status()
    return result

@app.get('/data/json')
def get_to_jsonl(month, year):
    result = files.FileSearch(month=month, year=year).reard_to_jsonl()
    return result

@app.get('/data/csv')
def get_to_csv(month, year):
    result = files.FileSearch(month=month, year=year).reard_to_csv()
    return result