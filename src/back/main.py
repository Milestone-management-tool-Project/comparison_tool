import fastapi
import fastapi.middleware.cors
import src.back.goals as goals, src.back.times as times
import src.back.file_operations as files
from typing import Annotated

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

@app.post("/goals/save")
def goals_set(goal:Annotated[list[str], fastapi.Form()], limit, month):
    result = goals.Goals(goal, status=None, limit=limit,month=month).save()
    return result

@app.post("/goals/update")
def goals_update(key, status, limit, month):
    result = goals.Goals(key=key, status=status, limit=limit, month=month).update()
    return result

@app.get('/data/json')
def get_to_jsonl(month, year):
    result = files.FileSearch(month=month, year=year).reard_to_jsonl()
    return result

@app.get('/data/csv')
def get_to_csv(month, year):
    result = files.FileSearch(month=month, year=year).reard_to_csv()
    return result