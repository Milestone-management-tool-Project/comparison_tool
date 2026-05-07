import { StatisticalArea } from "./components";
import { api } from "./api_instans";
export class Timer{
    timer: HTMLElement;
    operation_area: HTMLElement;
    start_timer: HTMLButtonElement;
    end_timer: HTMLButtonElement;
    timer_click: number;
    low_area:HTMLElement;
    log_area: HTMLElement;
    button_log: HTMLElement;
    csv_area: HTMLElement;
    left_area: HTMLElement;
    right_area: HTMLElement;
    csv_table: HTMLElement;
    csv_header: HTMLElement;
    csv_body: HTMLElement;

    constructor(){
        this.left_area = document.createElement('div')
        this.left_area.classList.add('left-area')
        this.right_area = document.createElement('div')
        this.right_area.classList.add('right-area')

        this.timer = document.createElement('div');
        this.timer.classList.add('timer');
        this.timer.id = 'timer'
        this.timer.textContent = '00:00:00'
        this.timer.style.textAlign = 'center'

        this.low_area = document.createElement('div')
        this.low_area.classList.add('low-area')

        this.log_area = document.createElement('div')
        this.log_area.classList.add('log-area')
        this.log_area.style.flexDirection = 'column'
        
        this.operation_area = document.createElement('div')
        this.operation_area.classList.add('operation_area')
        this.operation_area.id = 'operation_area'

        this.start_timer = document.createElement('button');
        this.start_timer.classList.add('start');
        this.start_timer.id = 'start'
        this.start_timer.textContent = 'start'
        this.start_timer.style.whiteSpace = 'nowrap'

        this.end_timer = document.createElement('button');
        this.end_timer.classList.add('end');
        this.end_timer.id = 'end'
        this.end_timer.textContent = 'stop'
        this.end_timer.style.whiteSpace = 'nowrap'

        this.button_log = document.createElement('div')
        this.button_log.classList.add('button-log')
        this.button_log.style.whiteSpace = "pre-wrap"
        this.button_log.id = 'button-log'

        this.csv_area = document.createElement('div')
        this.csv_area.classList.add('csv-area')

        this.csv_table = document.createElement('table')
        this.csv_table.classList.add('csv-table')
        this.csv_header = document.createElement('thead')
        this.csv_body = document.createElement('tbody')
        this.csv_body.classList.add('csv-body')
        this.timer_click = 0
    }

    private async _click_button(){
        const start_data = (await api.timer.timerStartTimerStartGet()).data
        this.button_log.append(start_data)
    }


    private async _csv_log(){
        const csv_data = (await api.timer.todayTimerTimerTodayGet()).data
        this.csv_body.innerHTML = ''
        csv_data.forEach((row: String) => {
            const tr = document.createElement('tr')
            const data1 = row[1]
            const data3 = row[3]
            const data4 = row[4]
            const td1 = document.createElement('td')
            td1.classList.add('td1')
            const td3 = document.createElement('td')
            td3.classList.add('td3')
            const td4 = document.createElement('td')
            td4.classList.add('td4')
            td1.textContent = data1 +' / '
            td3.textContent = data3 +' / '
            td4.textContent = data4
            tr.appendChild(td1)
            tr.appendChild(td3)
            tr.appendChild(td4)
            this.csv_body.appendChild(tr)
            
            
        });
    }

    
    async render(){
        const container = document.querySelector('.main-area');

        // csv-area
        const header = document.createElement('tr')
        const start_time = document.createElement('td')
        start_time.textContent = 'start-time / '
        const end_time = document.createElement('td')
        end_time.textContent = 'end-time / '
        const total = document.createElement('td')
        total.textContent = 'total'
        header.append(start_time)
        header.append(end_time)
        header.append(total)
        this.csv_header.append(header)
        this.csv_table.append(this.csv_header)
        this.csv_table.append(this.csv_body)
        this.csv_area.append(this.csv_table)

        // timer count
        let count = 0;

        // Statistics area
        const damyElement = document.createElement('div')
        damyElement.textContent = 'Statistics area'
        const Statistical = new StatisticalArea(damyElement);
        let isTracking: boolean = false;
        this._csv_log()
        
        // start
        this.start_timer.addEventListener("click", () => {
            if(isTracking === true){
                alert('It has already started.')
                return
            }
            clearInterval(this.timer_click)
            count = 0

            this._click_button()
            isTracking = !isTracking
            this.timer_click = setInterval(() => {
            count++;
            const h = Math.floor(count / 3600)
            const m = Math.floor((count % 3600) / 60)
            const s = count % 60
            this.timer.textContent = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0')}, 1000)


        })
        this.operation_area?.append(this.start_timer)

        // stop
        this.end_timer.addEventListener("click", () => {
            if(isTracking === false){
                alert('Not started')
                return
            }
            api.timer.timerEndTimerStopPost()
            isTracking = !isTracking
            clearInterval(this.timer_click)
            this._csv_log()
        })
        this.log_area.append(this.button_log)

        this.operation_area.append(this.start_timer)
        this.operation_area.append(this.end_timer)
        this.log_area.append(Statistical.data)
        this.left_area.append(this.operation_area, this.log_area)
        this.low_area.append(this.left_area)
        this.right_area.append(this.csv_area)
        this.low_area.append(this.right_area)
        container?.append(this.low_area)
    }
}