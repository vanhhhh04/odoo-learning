/** @odoo-module **/
import { registry } from '@web/core/registry';
const { Component, useState, onWillStart, useRef } = owl;
import { useService } from "@web/core/utils/hooks";

export class OwlTodoList extends Component {
    setup(){
        this.state = useState({
            task:{name:"", color:"#FF0000", completed:false},
            taskList:[],
            isEdit: false,
            activeId: false,
        })
        this.orm = useService("orm"),
        this.model = "owl.todo",
        this.searchInput = useRef("search-input")

        onWillStart(async ()=>{
            await this.getAllTasks()
        })
    }
        async getAllTasks(){
            this.state.taskList = await this.orm.searchRead(this.model, [], ["name", "color", "completed"])
        }

        addTask(){
            this.resetForm()
            this.state.activeId = false 
            this.state.isEdit = false 
        }

        editTask(task){
            this.state.activeId = task.id
            this.state.isEdit = true
            this.state.task = {...task}

        }

        async saveTask(){
            if (!this.state.isEdit){
                await this.orm.create(this.model, [this.state.task])
            } else {
                await this.orm.write(this.model, [this.state.activeId], this.state.task)
            }
            await this.getAllTasks()
        }

        resetForm(){
            this.state.task = {name:"", color:"#FF0000", completed:false}
        }

        async deleteTask(task){
            await this.orm.unlink(this.model, [task.id])
            await this.getAllTasks()

        }

        async searchTasks(){
            const text = this.searchInput.el.value
            console.log(text)
            this.state.taskList = await this.orm.searchRead(this.model, [['name','ilike', text]], ["name", "color", "completed"])
        }
}

OwlTodoList.template = 'todo.TodoList'
registry.category('actions').add('todo.action_todo_list_js', OwlTodoList);

