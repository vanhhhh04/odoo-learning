/** @odoo-module **/
import { registry } from '@web/core/registry';
const { Component, useState } = owl;

export class OwlTodoList extends Component {
    setup(){
        this.state = useState({
            taskList:[
                {id:1, name:"Task 1", color:"#FF000", completed: true},
                {id:2, name:"Task 2", color:"#FF000", completed: true},
                {id:3, name:"Task 3", color:"#FF000", completed: false},
            ]
        })
    }
}

OwlTodoList.template = 'todo.TodoList'
registry.category('actions').add('todo.action_todo_list_js', OwlTodoList);

