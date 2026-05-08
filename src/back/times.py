import csv
from datetime import datetime
import os
from .file_operations import create_path
from .file_operations import FileSearch
class TimeCheker():
    def __init__(self):
            self.flag = False

    def start_checker(self):
        
        if self.flag is True:
            return "not end"
        else:
            start_time = datetime.now()
            self.start = start_time
            self.flag = True
            return_time = datetime.now().strftime('%H:%M:%S')
            return 'start time is: ' + return_time

    def end_checker(self):
            if self.flag is False:
                 return "not start"
            else:
                self.endtime = datetime.now()
                self.total = self.endtime - self.start 
                result = self.save_to_csv()
                self.flag = False
                return result
    
    def save_to_csv(self):
        year_month = datetime.now().strftime("%Y-%m")
        path = f"csv/time_{year_month}.csv"
        
        full_path = create_path(path)
        if not os.path.exists(create_path('csv/')):
             os.mkdir(create_path('csv/'))
        file = os.path.isfile(full_path)

        try:
            with open(full_path, 'a', encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file:
                    writer.writerow(["start-date", "start-time","end-date", "end-time","total"])
                start_date = self.start.strftime("%Y-%m-%d")
                start_time = self.start.strftime("%H:%M:%S")
                end_date = self.endtime.strftime("%Y-%m-%d")
                end_time = self.endtime.strftime("%H:%M:%S")
                duration = str(self.total).split(".")[0]
                data = [start_date ,start_time, end_date, end_time ,duration]
                writer.writerow(data)
            
            return str(self.total).split(".")[0]
        except Exception as e:
             return f"Problems occurred with saving the CSV file.{e}"
    
    def import_to_csv(self):
         year = datetime.now().strftime('%Y')
         month = datetime.now().strftime('%m')
         data = FileSearch(year=year, month=month).reard_to_csv()
         times = data[1:]
         target = datetime.now().strftime("%Y-%m-%d")
         return_data = [row for row in times if row[0] == target]
         print(return_data)
         return return_data