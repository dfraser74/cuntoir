function getCookie(name){
    var name = name + "=";
    var cookieJar = document.cookie;
    var cookieList = cookieJar.split(";");
    for(var i = 0; i < cookieList.length; i++){
        var cookie = cookieList[i];
        while (cookie.charAt(0) == " ") {
            cookie = cookie.substring(1);
        }
        if(cookie.indexOf(name) == 0){
            return(cookie.substring(name.length, cookie.length));
        }
    }
    return(0)
}

function setCookie(name, value){
    currTime = (new Date).getTime();
    expireTime = currTime + 60*60*24*1000;
    expireString = (new Date(expireTime)).toUTCString();
    document.cookie = name + "=" + value +";"+"expires=" + expireString +";";
}

function makePostRequest(url, requestParams, method){
    url = "/dev/"
    $.ajax({
        type: "POST",
        url: url,
        data: requestParams,
        success: function(data){handleRequestReturn(data, method);}
    });
}

function makeGetRequest(url, requestParams, method){
    url = "/dev/"
    $.ajax({
        type: "GET",
        url: url,
        data: requestParams,
        success: function(data){handleRequestReturn(data, method);}
    });
}

function handleRequestReturn(data, method){
    if(method == "getAll"){
        handleGetAllReturn(data);
    }
    if(method == "loginPost"){
        handleLoginPostReturn(data);
    }
    if(method == "addTaskPost"){
        handleAddTaskPostReturn(data);
    }
    if(method == "createUser"){
        handleCreateUserReturn(data);
    }
    if(method == "completeTask"){
        handleCompleteTaskPostReturn(data);
    }
    if(method == "editTaskPost"){
        handleEditTaskPostReturn(data);
    }
    if(method == "getTaggedPost"){
        handleGetTaggedReturn(data);
    }
    if(method == "search"){
        handleSearchPostReturn(data);
    }
    if(method == "dateSearch"){
        handleDateSearchPostReturn(data);
    }
    if(method == "getTaskDates"){
        renderCal(data);
    }
}

function getAll(){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    if(username == 0 || authCode == 0){
        window.location = "login.html"
    }else{
        var data = {"username":username, "authCode":authCode, "method":"getAll", "sort":"default"};
        makePostRequest("/", data, "getAll");
    }
}

function handleGetAllReturn(data){
    if(data == 0){
        window.location = "login.html"
    }
    if(data == 2){
        document.getElementById("tasks").innerHTML = "<div class='task'><h2 class='taskTitle'>You're all done, congrats!!</h2></div>";
    }
    if(data != 0 && data != 2){
        document.getElementById("tasks").innerHTML = data;
    }
}

function loginPost(username, pass){
    username = username.trim();
    pass = pass.trim();
    setCookie("username", username)
    var data = {"username":username, "userPass":pass, "method":"login"};
    makePostRequest("/", data, "loginPost");
}

function handleLoginPostReturn(data){
    if(data != 0){
        setCookie("authCode", data);
        window.location = "index.html";
    }
    else{
        document.getElementById("info").innerHTML = "Username or password incorrect";
    }
}

function addTaskPost(title, description, dueTime, tags){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    if(title == ""){
        document.getElementById("info").innerHTML = "Your task needs a title";
    }else{
        if(dueTime != 0){
            var data = {"method":"addTask", "username":username, "authCode":authCode, "dueTime":dueTime, "description":description, "title":title, "tags":tags};
            makePostRequest("/", data, "addTaskPost");
        }
    }
}

function handleAddTaskPostReturn(data){
    if(data == 1){
        closeAdd();
        getAll();
    }else{
        window.location = "login.html";
    }
}

function getDateTime(dateString, timeString){
    day = dateString.split("/")[0];
    month = dateString.split("/")[1];
    year = dateString.split("/")[2];
    hour = timeString.split(":")[0];
    minute = timeString.split(":")[1];
    second = 00;
    var time = new Date(year, month-1, day, hour, minute, second, 0).getTime();
    time = time/1000;
    if(isNaN(time)){
        document.getElementById("info").innerHTML = "Sorry, date format incorrect. It should be dd/mm/yyyy and hh/mm/ss";
        document.getElementById("editInfo").innerHTML = "Sorry, date format incorrect. It should be dd/mm/yyyy and hh/mm/ss";
        return(0)
    }
    return(time)
}

function getCurrDateString(){
    var dateString = "";
    var currentDate = new Date();
    var day = currentDate.getDate() + 1;
    var month = currentDate.getMonth() + 1;
    var year = currentDate.getFullYear();
    dateString = day+"/"+month+"/"+year
    return(dateString)
}

function getCurrTimeString(){
    var timeString = "";
    var currentDate = new Date();
    var hour = currentDate.getHours();
    var minute = currentDate.getMinutes();
    var second = currentDate.getSeconds();
    if(minute < 10){
        minute = "0" + minute;
    }
    if(hour < 10){
        hour = "0" + hour;
    }
    timeString = hour + ":" + minute;
    return(timeString);
}

function createUser(username, pass, pass2, inviteCode){
    username = username.trim();
    pass = pass.trim();
    pass2 = pass2.trim();
    if(pass == pass2){
        var data = {"method":"createUser", "username":username, "userPass":pass, "inviteCode":inviteCode};
        makePostRequest("/", data, "createUser");
    }else{
        document.getElementById("info").innerHTML = "Passwords Don't Match";
    }
}

function handleCreateUserReturn(data){
    if(data == 1){
        window.location = "login.html";
    }
    if(data == 0){
        document.getElementById("info").innerHTML = "Invite Code Incorrect";
    }
    if(data == 2){
        document.getElementById("info").innerHTML = "Username Taken";
    }
}

function completeTaskPost(title, createTime){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    document.getElementById(title).style.display = "none";
    var data = {"method":"completeTask", "title":title, "createTime":createTime, "username":username, "authCode":authCode};
    makePostRequest("/", data, "completeTask");
}

function handleCompleteTaskPostReturn(data){
    if(data == 1){
        getAll();
    }
}

function logout(){
    setCookie("authCode", "0");
    setCookie("username", "0");
    window.location = "login.html";
}

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    closeAdd();
    closeEdit();
    closeCalBar();
    document.getElementById("navInfo").innerHTML = "";
    document.getElementById("searchInput").value = "";
    document.getElementById("searchInput").focus();
    if(document.getElementById("nav").style.width != "0px"){
        closeNav();
        return;
    }
    if(window.screen.availWidth < 500){
        document.getElementById("nav").style.width = "100%";
    }else{
        document.getElementById("nav").style.width = "300px";
        document.getElementById("main").style.marginLeft = "300px";
    }
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("nav").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
}

function openAdd(){
    closeNav();
    closeEdit();
    closeCalBar();
    document.getElementById("title").value = "";
    document.getElementById("description").value = "";
    document.getElementById("tags").value = "";
    document.getElementById("info").value = "";
    if(document.getElementById("add").style.width != "0px"){
        closeAdd();
        return;
    }
    if(window.screen.availWidth < 500){
        document.getElementById("add").style.width = "100%";
        document.getElementById("title").focus();
    }else{
        document.getElementById("title").focus();
        document.getElementById("add").style.width = "300px";
        document.getElementById("main").style.marginLeft = "300px";
    }
    document.getElementById("dateString").value = getCurrDateString();
    document.getElementById("timeString").value = getCurrTimeString();
}

function closeAdd(){
    document.getElementById("add").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
    hideDatePicker("addDatePicker");
}

function openEdit(title, description, dueTimeString, createTime, tags){
    closeNav();
    closeAdd();
    closeCalBar();
    document.getElementById("editInfo").innerHTML = "";
    if(document.getElementById("edit").style.width != "0px" && document.getElementById("editTitle").value == title){
        closeEdit();
        return;
    }
    if(window.screen.availWidth < 500){
        document.getElementById("edit").style.width = "100%";
        document.getElementById("editTitle").focus();
    }else{
        document.getElementById("editTitle").focus();
        document.getElementById("edit").style.width = "300px";
        document.getElementById("main").style.marginLeft = "300px";
    }
    updateEditFields(title, description, dueTimeString, createTime, tags);
}

function closeEdit(){
    document.getElementById("edit").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
    hideDatePicker("editDatePicker");
}

function updateEditFields(title, description, timeString, createTime, tags){
    var date = timeString.split(" ")[0]
    var time = timeString.split(" ")[1]
    document.getElementById("editTitle").value = title;
    document.getElementById("editDescription").value = description;
    document.getElementById("editDateString").value = date;
    document.getElementById("editTimeString").value = time;
    document.getElementById("editInfo").innerHTML = "";
    document.getElementById("editCreateTime").innerHTML = createTime;
    document.getElementById("editTags").value = tags;
}

function editTaskPost(title, description, dueTime, tags){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var createTime = document.getElementById("editCreateTime").innerHTML;
    if(title == ""){
        document.getElementById("editInfo").innerHTML = "Your task needs a title";
    }else{
        if(dueTime != 0){
            var data = {"method":"editTask", "username":username,"dueTime":dueTime, "authCode":authCode, "createTime":createTime, "description":description, "title":title, "tags":tags};
            makePostRequest("/", data, "editTaskPost");
        }
    }
}
function handleEditTaskPostReturn(data){
    if(data == 1){
        closeEdit();
        getAll();
    }
    if(data == 0){
        window.location = "login.html";
    }
}

function getTagged(tag){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    if(username == 0 || authCode == 0){
        window.location = "login.html"
    }else{
        var data = {"username":username, "authCode":authCode, "method":"getTagged", "sort":"default", "tag":tag};
        makePostRequest("/", data, "getTaggedPost");
    }
}

function handleGetTaggedReturn(data){
    if(data == 0){
        window.location = "login.html"
    }
    if(data == 2){
        document.getElementById("tasks").innerHTML = "<div class='task'><h2 class='taskTitle'>No tasks with that tag</h2><input type='button' value='Go Back' onclick='getAll();'></div>";
        scroll(0,0);
    }
    if(data != 0 && data != 2){
        document.getElementById("tasks").innerHTML = data;
        scroll(0,0);
    }
}

function searchPost(searchString){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    if(searchString.length < 1){
        document.getElementById("navInfo").innerHTML = "You need to search for something!";
        return;
    }
    closeNav();
    if(username == 0 || authCode == 0){
        window.location = "login.html"
    }else{
        var data = {"username":username, "authCode":authCode, "method":"search", "sort":"default", "searchString":searchString};
        makePostRequest("/", data, "search");
    }
}

function handleSearchPostReturn(data){
    if(data == 0){
        window.location = "login.html"
    }
    if(data == 2){
        document.getElementById("tasks").innerHTML = "<div class='task' style='height:auto;'><h2 class='taskTitle'>No matches</h2><input type='button' value='Go Back' onclick='getAll();'></div>";
        scroll(0,0);
    }
    if(data != 0 && data != 2){
        document.getElementById("tasks").innerHTML = data;
        scroll(0,0);
    }
}

function openCalBar(){
    closeAdd();
    closeEdit();
    closeNav();
    var month = new Date().getMonth();
    if(document.getElementById("calBar").style.width != "0px"){
        closeCalBar();
        return;
    }
    if(window.screen.availWidth < 500){
        document.getElementById("calBar").style.width = "100%";
    }else{
        document.getElementById("calBar").style.width = "300px";
        document.getElementById("main").style.marginLeft = "300px";
    }
    renderCalPost(month);
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeCalBar() {
    document.getElementById("calBar").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
}

function renderCalPost(monthInt){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    if(navigator.onLine == true){
        if(username == 0 || authCode == 0){
            window.location = "login.html"
        }else{
            var data = {"username":username, "authCode":authCode, "method":"getTaskDates", "sort":"default", "month":monthInt};
            makePostRequest("/", data, "getTaskDates");
        }
    }
    else{
        dueTimeList = document.getElementsByClassName("dueTime")
        var i = 0;
        var datesString = "";
        while(i < dueTimeList.length){
            datesList = dueTimeList[i].innerHTML.split(" ")[0].split("/").slice(0, 2);
            datesString += datesList[0] + "/" + datesList[1] + ",";
            i += 1;
        }
        console.log(monthInt + ";" + datesString);
        renderCal(monthInt + ";" + datesString);
    }
}

function renderCal(data){
    if(data == 0){
        window.location = "login.html";
        return;
    }
    else{
        var monthInt = parseInt(data.split(";")[0]);
        var datesList = data.split(";")[1].split(",");
        var ii = 0;
        var parsedDatesList = "";
        while(ii < datesList.length){
            day = parseInt(datesList[ii].split("/")[0]);
            month = parseInt(datesList[ii].split("/")[1])-1;
            parsedDatesList += day+"/"+month;
            ii += 1;
        }
        console.log(parsedDatesList);
        console.log(datesList);
    }
    while(monthInt > 11){
        monthInt -= 12;
    }
    while(monthInt < 0){
        monthInt += 12
    }
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var monthName = monthNames[monthInt];
    var year = new Date().getFullYear();
    var firstDay = new Date(year, monthInt, 1).getDay();
    var lastDate = new Date(year, monthInt + 1, 0).getDate();
    var i = 0;
    var n = 0;
    document.getElementById("calHead").innerHTML = "<i class='fa fa-arrow-left' onclick='renderCalPost(" + (monthInt-1) + ");'></i>" + monthName + " " + year + "<i class='fa fa-arrow-right' onclick='renderCalPost(" + (monthInt+1) + ");'></i>";
    var innerHTML = "<tbody><tr id='dayNamesRow'>";
    while(i < 7){
        innerHTML += "<th class='dayName'>" + dayNames[i] + "</th>"
        i += 1;
    }
    innerHTML += "</tr>"
    startDay = firstDay;
    i = 1;
    innerHTML += "<tr>";
    while(i < startDay+1){
        innerHTML += "<td class='noDate'></td>"
        i += 1;
    }
    i = 1;
    while(i < 8-startDay){
        console.log(i+"/"+monthInt + " : " + parsedDatesList + " : " + parsedDatesList.indexOf(i+"/"+monthInt));
        if(parsedDatesList.indexOf(i+"/"+monthInt) >= 0){
            innerHTML += "<td class='activeDate' onclick='dateSearch(" + i + ", " + monthInt + ");'>" + i + "</td>";
        }
        else{
            innerHTML += "<td onclick='dateSearch(" + i + ", " + monthInt + ");'>" + i + "</td>";
        }
        i += 1;
    }
    innerHTML += "</tr>";
    while(i <= lastDate){
        innerHTML += "<tr>";
        n = 0;
        while(n < 7 && i <= lastDate){
            if(parsedDatesList.indexOf(i+"/"+monthInt) >= 0){
                innerHTML += "<td class='activeDate' onclick='dateSearch(" + i + ", " + monthInt + ");'>" + i + "</td>";
            }
            else{
                innerHTML += "<td onclick='dateSearch(" + i + ", " + monthInt + ");'>" + i + "</td>";
            }
            n += 1;
            i += 1;
        }
        innerHTML += "</tr>";
    }
    innerHTML += "<tbody>";
    document.getElementById("calBody").innerHTML = innerHTML;
}

function dateSearch(dateInt, monthInt){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    closeCalBar();
    var year = new Date().getFullYear();
    var lowerTime = new Date(year, monthInt, dateInt, 0, 0, 0, 0).getTime()
    lowerTime = lowerTime/1000;
    var upperTime = new Date(year, monthInt, dateInt+1, 0, 0, 0, 0).getTime()
    upperTime = upperTime/1000;
    if(username == 0 || authCode == 0){
        window.location = "login.html"
    }else{
        var data = {"username":username, "authCode":authCode, "method":"dateSearch", "sort":"default", "lowerTime":lowerTime, "upperTime":upperTime};
        makePostRequest("/", data, "dateSearch");
    }
}

function handleDateSearchPostReturn(data){
    if(data == 0){
        window.location = "login.html"
    }
    if(data == 2){
        document.getElementById("tasks").innerHTML = data;
        scroll(0,0);
    }
    if(data != 0 && data != 2){
        document.getElementById("tasks").innerHTML = data;
        scroll(0,0);
    }
}
function renderDatePicker(monthInt, divId, tableId, headId, inputId){
    document.getElementById(divId).style.display = "inline-block";
//    document.getElementById(divId).style.position = "absolute";
    document.getElementById(divId).style.height = "80%";
    while(monthInt > 11){
        monthInt -= 12;
    }
    while(monthInt < 0){
        monthInt += 12
    }
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var monthName = monthNames[monthInt];
    var year = new Date().getFullYear();
    var firstDay = new Date(year, monthInt, 1).getDay();
    var lastDate = new Date(year, monthInt + 1, 0).getDate();
    var i = 0;
    var n = 0;
    document.getElementById(headId).innerHTML = "<i class='fa fa-arrow-left' onclick='renderDatePicker("+(monthInt-1)+",\""+divId+"\",\""+tableId+"\",\""+headId+"\",\""+inputId+"\");'></i>" + monthName + " " + year + "<i class='fa fa-arrow-right' onclick='renderDatePicker(" + (monthInt+1) + ",\""+divId+"\",\""+tableId+"\",\""+headId+"\",\""+inputId+"\");'></i>";
    var innerHTML = "<tbody><tr id='dayNamesRow'>";
    while(i < 7){
        innerHTML += "<th class='dayName'>" + dayNames[i] + "</th>"
        i += 1;
    }
    innerHTML += "</tr>"
    startDay = firstDay;
    i = 1;
    innerHTML += "<tr>";
    while(i < startDay+1){
        innerHTML += "<td class='noDate'></td>"
        i += 1;
    }
    i = 1;
    while(i < 8-startDay){
        innerHTML += "<td onclick='updateDateInput(\""+inputId+"\","+i+","+(monthInt+1)+",\""+year+"\");'>" + i + "</td>";
        i += 1;
    }
    innerHTML += "</tr>";
    while(i <= lastDate){
        innerHTML += "<tr>";
        n = 0;
        while(n < 7 && i <= lastDate){    
            innerHTML += "<td onclick='updateDateInput(\""+inputId+"\","+i+","+(monthInt+1)+",\""+year+"\");'>" + i + "</td>";
            n += 1;
            i += 1;
        }
        innerHTML += "</tr>";
    }
    innerHTML += "<tbody>";
    document.getElementById(tableId).innerHTML = innerHTML;
}

function hideDatePicker(divId){
    document.getElementById(divId).style.display = "none";
}

function updateDateInput(id, day, month, year){
    document.getElementById(id).value = day+"/"+month+"/"+year;
}
