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
    ev.dataTransfer.setData("text", ev.target.id);
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var encodedTaskName = encodeURIComponent(document.getElementById(data).innerText);
    if (ev.target.id != "kanban-delete"){
        ev.target.appendChild(document.getElementById(data));
    } else {
        var delTask = confirm("Remove task: \"" + document.getElementById(data).innerText + "\"?");
        if (delTask) {
            document.getElementById(data).remove();
        } else {
            return;
        }
    }
    taskChangeState(encodedTaskName, ev.target.id);
}


/* ==================
Task Functionality (object, create, delete)
================== */

function createTask(taskName, taskStartDate, taskDueDate, taskProgress, source) {
    if (source === "user"){
        taskCreateEndpoint = "/create/task?uid=" + window.userID + 
                            "&taskName=" + taskName + 
                            "&taskStartDate=" + taskStartDate +
                            "&taskDueDate=" + taskDueDate +
                            "&taskProgress=" + taskProgress;

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
    
        req.open('POST', taskCreateEndpoint, true);
        req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        req.send();
    }

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

function userCreateTask() {
    var taskName = prompt("Enter a name for the task:");
    if (taskName === ""){
        alert("Task name cannot be empty!");
        return;
    }
    var taskStartDate = prompt("Enter a start date for the task in MM/DD/YYYY format:");
    var taskDueDate = prompt("Enter a due date for the task in MM/DD/YYYY format:");
    var alphaRegExp = /[a-zA-Z]/g;
    if ((taskStartDate.length != 10 || taskDueDate.length != 10) || 
        (alphaRegExp.test(taskStartDate) || alphaRegExp.test(taskDueDate))) {
            alert("Failed to create task, invalid task dates! Needs to be in MM/DD/YYYY format!");
            return;
    }

    // Convert dates to epoch
    var epochStartDate = toEpoch(taskStartDate);
    var epochDueDate = toEpoch(taskDueDate);

    if (epochStartDate > epochDueDate) {
        alert("Failed to create task, invalid task dates! due date needs to be later than start date!");
        return;
    }
    var taskProgress = prompt("Enter the state of the task (\"To-Do\", \"In-Progress\", or \"Done\"):");
    switch(taskProgress.toLowerCase()) {
        case "to-do":
            createTask(taskName, epochStartDate, epochDueDate, "todo", "user");
            break;
        case "in-progress":
            createTask(taskName, epochStartDate, epochDueDate, "inprog", "user");
            break;
        case "done":
            createTask(taskName, epochStartDate, epochDueDate, "done", "user");
            break;
        default:
            alert("Failed to create task, invalid task state! Needs to be (\"To-Do\", \"In-Progress\", or \"Done\").");
            return;
    }
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

    tasksChangeEndpoint = "/user/tasks/edit?uid=" + window.userID + "&taskName=" + taskName + "&newState=" + formNewState;

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


// UTILS
function toEpoch (date) {
    return Date.parse(date);
}