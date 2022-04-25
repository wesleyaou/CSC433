// Number of total kanban tasks
window.kanbanTasks = 0;
window.userID = 2;
window.userTasks = [];

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
        console.log(ev.target.id);
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
            kanbanCol = document.getElementById("inprog-content");
            break;
        case "done":
            kanbanCol = document.getElementById("done-content");
            break;
        case "todo":
        default:
            kanbanCol = document.getElementById("todo-content");
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
    else if (taskName == null) {
        return;
    }
    var taskStartDate = prompt("Enter a start time for the task in MM/dd/yyyy hh:mm format:");
    var taskDueDate = prompt("Enter a end time for the task in MM/dd/yyyy hh:mm format:");
    var alphaRegExp = /[a-zA-Z]/g;
    if (taskStartDate == null || taskDueDate ==null){
        return;
    }
    else if ((taskStartDate.length != 16 || taskDueDate.length != 16) || 
        (alphaRegExp.test(taskStartDate) || alphaRegExp.test(taskDueDate))) {
            alert("Failed to create task, invalid task dates! Needs to be in MM/dd/yyyy hh:mm format!");
            return;
    }

    // Convert dates to epoch
    var epochStartDate = toEpoch(taskStartDate);
    var epochDueDate = toEpoch(taskDueDate);

    if (epochStartDate > epochDueDate) {
        alert("Failed to create task, invalid task dates! due date needs to be later than start date!");
        return;
    }
    var taskProgress = prompt("Enter the state of the task (\"To-Do\", \"In-Progress\", or \"Done\"):", "To-Do");
    
    if (taskProgress == null){
        return;
    }
    
    switch(taskProgress.toLowerCase()) {
        case "to-do":
            addTask(taskName, epochStartDate, epochDueDate, "todo");
            pullUserTasks();
            break;
        case "in-progress":
            addTask(taskName, epochStartDate, epochDueDate, "inprog");
            pullUserTasks();
            break;
        case "done":
            addTask(taskName, epochStartDate, epochDueDate, "done");
            pullUserTasks();
            break;
        default:
            alert("Failed to create task, invalid task state! Needs to be (\"To-Do\", \"In-Progress\", or \"Done\").");
            return;
    }
}

// Function to populate all kanban board tasks
function populateKanban() {
    taskArray = window.userTasks;

    clearKanban();

    if(taskArray.length > 0) {
        for(var i=0; i < taskArray.length; i++){
            createTask(taskArray[i]["taskName"], taskArray[i]["taskStartDate"], taskArray[i]["taskDueDate"], taskArray[i]["taskProgress"]);
        }
    }
}

function clearKanban(){
    var kanbanCols = document.getElementsByClassName("kanban-content");

    for (i=0; i < kanbanCols.length; i++) {
        kanbanCols[i].innerHTML = ""
    }
}

function taskChangeState(taskName, newState){

    // Handle state changes and deletes
    var formNewState = newState.replace("-content", "").replace("kanban-", "");

    console.log(formNewState);

    tasksChangeEndpoint = encodeURI("/user/tasks/edit?uid=" + window.userID + "&taskName=" + taskName + "&newState=" + formNewState);

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


function pullUserTasks () {
    tasksEndpoint = "/user/tasks/uid=" + window.userID;

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
            if (JSON.stringify(window.userTasks.sort()) !== JSON.stringify(taskArray.sort())) {
                console.log("WINDOW TASKS: " + JSON.stringify(window.userTasks.sort()));
                console.log("AJAX TASKS: " + JSON.stringify(taskArray.sort()));
                window.userTasks = taskArray;
                populateKanban();
                createCalendar();
            }
            window.tasksForMonth = taskArray;
        }
    }

    req.open('POST', tasksEndpoint, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}


function addTask(taskName, taskStartDate, taskDueDate, taskProgress) {
    taskCreateEndpoint = encodeURI("/create/task?uid=" + window.userID + 
                        "&taskName=" + taskName + 
                        "&taskStartDate=" + taskStartDate +
                        "&taskDueDate=" + taskDueDate +
                        "&taskProgress=" + taskProgress).replace("#", "%23");
    

    // AJAX post to add user tasks
    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var ajaxReturn = JSON.parse(this.responseText);
            for (var key in ajaxReturn){
                if (key == "error") {
                    alert("Error returned trying to POST tasks: " + ajaxReturn["error"]);
                }
            }
        }
    }

    req.open('POST', taskCreateEndpoint, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}

/* ==================
Calendar Functionality
================== */

function createCalendar() {
    clearCalendar();

    var date = new Date();
    var monthName = getStringMonth(date.getMonth());
    var monthLen = getLastDayOfMonth(date.getFullYear(), date.getMonth());

    var calContainer = document.createElement("div");
    calContainer.id = "cal-container";
    var calHeader = document.createElement("h2");
    calHeader.innerText = monthName;
    var calBody = createCalendarStructure(monthLen, date);

    calContainer.append(calHeader);
    calContainer.append(calBody);

    var mainCal = document.getElementById("cal-display");
    mainCal.append(calContainer);
    mainCal.append(createTaskList(date));

    // Make it clickable
    eventAddCal();

}

function clearCalendar() {
    var mainCal = document.getElementById("cal-display");
    mainCal.innerHTML = "";
}

// Creates the table for the calendar
function createCalendarStructure(monthLen, date) {
    var calTable = document.createElement("table");
    calTable.align = "center";
    // calTable.cellPadding = 12;
    // calTable.cellSpacing = 12;

    var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

    // Create the calendar head
    var calHead = document.createElement("thead");
    for (i=0; i < days.length; i++) {
        headDayDom = document.createElement("th");
        headDayDom.innerHTML = days[i];

        calHead.append(headDayDom);
    }

    var monthFirstDay = new Date(date.getFullYear(), date.getMonth(), "01").getDay();
    var weeksInMonth = Math.ceil((monthLen + monthFirstDay) / 7);

    var daysAddedIter = 0;
    var calBody = document.createElement("tbody");
    for (week=0; week < weeksInMonth; week++) {
        var weekDom = document.createElement("tr");
        for (day=0; day < 7; day++) {
            var dayText = document.createTextNode("");
            var dayDom = document.createElement("td");
            if ((daysAddedIter == 0 && monthFirstDay == day) ||
                (monthLen > daysAddedIter && daysAddedIter > 0)) {
                dayDom.id = "cal-" + (daysAddedIter + 1);
                dayDom.className = "cal-day";
                daysAddedIter++;
                dayText = document.createTextNode(daysAddedIter)
                if(date.toLocaleDateString().split("/")[1] == daysAddedIter){
                    dayDom.className += " today";
                }
            }
            dayDom.appendChild(dayText)
            weekDom.append(dayDom);
        }
        calBody.append(weekDom);
    }

    calTable.append(calHead);
    calTable.append(calBody);

    return calTable;
}

function createTaskList(currentDate) {
    tasksForMonth = getTasksForMonth(currentDate);

    var taskListDiv = document.createElement("div");
    taskListDiv.className = "task-list";

    var taskListDom = document.createElement("ul");
    if(tasksForMonth.length > 0) {
        for (i=0; i < tasksForMonth.length; i++){
            var taskItemDom = document.createElement("li");
            var taskNameDom = document.createElement("p");
            taskNameDom.appendChild(document.createTextNode(tasksForMonth[i]["taskName"]))
            var taskDueDom = document.createElement("p");
            var taskDueDate = new Date((parseInt(taskArray[i]["taskDueDate"]) * (10 ** 3))).toLocaleDateString();
            console.log("TASK DUE: " + taskDueDate);
            taskDueDom.appendChild(document.createTextNode(taskDueDate));
            taskItemDom.className = "task-list-item cal-" + taskDueDate.split("/")[1]
            var taskProgDom = document.createElement("p");
            taskProgDom.appendChild(document.createTextNode(tasksForMonth[i]["taskProgress"]));

            taskItemDom.appendChild(taskNameDom);
            taskItemDom.appendChild(taskDueDom);
            taskItemDom.appendChild(taskProgDom);
            taskListDom.appendChild(taskItemDom);
        }
    } else {
        var taskItemDom = document.createElement("li");
        var noTasksDom = document.createElement("p");
        noTasksDom.appendChild(document.createTextNode("No tasks found for this month!"));
        taskListDom.appendChild(noTasksDom);
    }

    taskListDiv.append(taskListDom);

    return taskListDiv;
}

// Create event listeners for the calendar
function eventAddCal(){
    document.querySelectorAll('.cal-day').forEach(item => {
        item.addEventListener('click', event => {
          clickedCalDay(item.id);
        })
      })
}

// Function that handles a calendar day being selected
function clickedCalDay(monthDayDom) {
    taskList = document.getElementsByClassName("task-list-item");
    calDays = document.getElementsByClassName("cal-day");

    // Remove all active cal days/tasks
    for (i=0; i < taskList.length; i++) {
        if (taskList[i].className.includes("active-day")){
            taskList[i].className = taskList[i].className.replace(" active-day", "");
        }
    }

    for (i=0; i < calDays.length; i++) {
        if (calDays[i].className.includes("active-day")){
            calDays[i].className = calDays[i].className.replace(" active-day", "");
        }
    }

    console.log("MONTHDAY: " + monthDayDom);

    //monthDayDom = "cal-" + monthDay;
    console.log(monthDayDom);

    var calDay = document.getElementById(monthDayDom);
    var taskDay = document.getElementsByClassName(monthDayDom);

    calDay.className += " active-day";
 
    for (i=0; i < taskDay.length; i++) {
        console.log(taskDay[i]);
        taskDay[i].className += " active-day";
    }
}

// Calendar Utils
function getStringMonth(month) {
    var months = [ "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December" ];

    return months[month];
}

function getLastDayOfMonth(year, month) {
    return parseInt(new Date(year, month + 1, 0).toLocaleDateString().split("/")[1]);
}

function getTasksForMonth(currentDate) {
    var tasksForMonth = [];

    taskArray = window.userTasks;

    for(var i=0; i < taskArray.length; i++){
        var taskDueDate = new Date(parseInt(taskArray[i]["taskDueDate"]) * (10**3));
        console.log(taskDueDate)
        if ((taskDueDate.getMonth() == currentDate.getMonth()) || 
        (taskDueDate.getFullYear == currentDate.getFullYear())){
            console.log("PUSHING: " + taskArray[i]["taskName"]);
            tasksForMonth.push(taskArray[i]);
        }
    }

    return tasksForMonth;
}

/* ==================
Startup Behavior
================== */

function startStudentAssist() {
    selectDefault();
    pullUserTasks();
    createCalendar();
}


/* ==================
General Utils
================== */

function toEpoch (date) {
    return Date.parse(date) * (10**-3);
}


