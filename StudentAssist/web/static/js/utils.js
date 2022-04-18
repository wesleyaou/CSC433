// Number of total kanban tasks
window.kanbanTasks = 0;
window.userID = 2;


/* ==================
Tab Functionality
================== */

function openTab(evt, TabName) {
    // Declare all variables
    var i, tabContent, tabLinks;

    // Get all elements with class="tabcontent" and hide them
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tabLinks = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tabLinks.length; i++) {
        tabLinks[i].className = tabLinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(TabName).style.display = "flex";
    evt.currentTarget.className += " active";
}


function selectDefault() {
    // For default tab
    document.getElementById("home-btn").click();
}


/* ==================
Kanban Functionality (drag & drop)
================== */

function drag(ev) {
    console.log("drag event!");
    console.log(ev.target.id);
    ev.dataTransfer.setData("text", ev.target.id);
}

function allowDrop(ev) {
    console.log("allow drop event!");
    ev.preventDefault();
}

function drop(ev) {
    console.log(ev);
    //taskName = document.getElementById(target.id).innerText;
    //console.log(taskName);
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
    encodedTaskName = encodeURIComponent(document.getElementById(data).innerText);
    taskChangeState(encodedTaskName, ev.target.id);
}


/* ==================
Task Functionality (object, create, delete)
================== */

function createTask(taskName, taskStartDate, taskDueDate, taskProgress) {
    const task = new Object();

    task.taskName = taskName;
    task.taskStartDate = taskStartDate;
    task.taskDueDate = taskDueDate;
    task.taskProgress = taskProgress;

    // Create a new task div
    var taskText = document.createElement("span");
    taskText.innerHTML = task.taskName;

    var taskDiv = document.createElement("div");
    taskDiv.className = "kanban-task";
    taskDiv.id = "task" + window.kanbanTasks;
    taskDiv.draggable = true;
    taskDiv.append(taskText);

    taskDiv.addEventListener("dragstart", drag)


    switch(task.taskProgress) {
        case "inprog":
            kanbanCol = document.getElementById("kanban-inprog");
            break;
        case "done":
            kanbanCol = document.getElementById("kanban-done");
            break;
        case "todo":
        default:
            kanbanCol = document.getElementById("kanban-todo");
            break;

    }

    kanbanCol.append(taskDiv);

    // Add one to total kanban tasks
    window.kanbanTasks++;
}

// Function to populate all kanban board tasks
function populateKanban(uid) {
    tasksEndpoint = "/user/tasks/uid=" + uid

    // AJAX post to get all tasks
    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var ajaxReturn = JSON.parse(this.responseText);
            for (var key in ajaxReturn){
                if (key == "error") {
                    alert("Error returned trying to get tasks: " + ajaxReturn["error"]);
                }
            }
            taskArray = ajaxReturn["tasks"];
            for(var i=0; i < taskArray.length; i++){
                createTask(taskArray[i]["taskName"], taskArray[i]["taskStartDate"], taskArray[i]["taskDueDate"], taskArray[i]["taskProgress"]);
            }
        }
    }

    req.open('POST', tasksEndpoint, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}

function taskChangeState(taskName, newState){

    var formNewState = newState.replace("kanban-", "")

    tasksChangeEndpoint = "/user/tasks/edit/uid=" + window.userID + "&taskName=" + taskName + "&newState=" + formNewState;

    // AJAX post to get all tasks
    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var ajaxReturn = JSON.parse(this.responseText);
            for (var key in ajaxReturn){
                if (key == "error") {
                    alert("Error returned trying to update tasks: " + ajaxReturn["error"]);
                }
            }
        }
    }

    req.open('POST', tasksChangeEndpoint, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}
