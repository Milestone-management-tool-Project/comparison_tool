import { StatisticalArea } from "./components";
import { api } from "./api_instans";
export class Goals{
    goals: HTMLElement;
    goal_button: HTMLButtonElement[] = [];
    left_area: HTMLElement;
    goals_area: HTMLElement;
    right_area: HTMLElement;
    goal_entry_area: HTMLElement;
    goal_entry: HTMLInputElement[] = [];
    goal_set: HTMLElement[] = [];
    constructor(){
        this.goals_area = document.createElement('div')
        this.goals_area.classList.add('goals-area')
        //goal-view
        this.goals = document.createElement('div')
        this.goals.classList.add('goal-view')
        this.goals.textContent = 'goals area'

        //left-area
        this.left_area = document.createElement('div')
        this.left_area.classList.add('left-area')

        //right-area
        this.right_area = document.createElement('div')
        this.right_area.classList.add('right-area')
        this.goal_entry_area =  document.createElement('div')
        this.goal_entry_area.classList.add('goal-entry-area')
        for (let i = 0; i < 4; i++){
            const input_form = document.createElement('input')
            this.goal_entry.push(input_form)
            const goal_button = document.createElement('button')
            this.goal_button.push(goal_button)
            this.goal_set.push(input_form, goal_button)
        }
        
        
    }
    async render(){
        const damyElement = document.createElement('div')
        damyElement.textContent = 'Statistics area'
        const Statistical = new StatisticalArea(damyElement);
        Statistical.data.classList.add('statistics')

        const container = document.querySelector('.main-area')
        this.goal_entry_area.append(...this.goal_set)
        this.right_area.appendChild(this.goal_entry_area)
        this.left_area.append(this.goals, Statistical.data)
        this.goals_area.append(this.left_area, this.right_area)
        container?.append(this.goals_area)
    }
}