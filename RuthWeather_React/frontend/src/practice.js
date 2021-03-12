
var tasks = this.state.todoList
var self = this
..<div>
{tasks.map(function(task,index){
    return(
      <div key={index} className="task-wrapper flex-wrapper">

        <div onClick={() => self.strikeUnstrike(task)} style={{flex:7}}>

          {task.completed == false ? (
            <span>{task.title}</span>
          ) : (
            <strike>{task.title}</strike>
          )}
        </div>

        <div style={{flex:1}}>
            <button onClick={() => self.startEdit(task)} className="btn btn-sm btn-outline-info">Edit</button>
        </div>

        <div style={{flex:1}}>
            <button onClick={() => self.deleteItem(task)} className="btn btn-sm btn-outline-dark delete">Delete</button>
        </div>

      </div>
    )
})}
