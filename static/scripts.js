if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js')
    .then(function(reg) {
        // registration worked
        console.log("Service worker registered")
        reg.update()
        }).catch(function(error) {
        // registration failed
        console.log('Registration failed with ' + error);
    });
}

if(localStorage["duePosts"] == null){
    localStorage["duePosts"] = 0;
}

setInterval(clearCachedRequests, 1000)

thisBrowserSupportsPush = "true";

function updateSubButton(){
    document.getElementById("pushPermission").style.display = "block";
    if("serviceWorker" in navigator){
        navigator.serviceWorker.getRegistration().then(function(reg){
            reg.pushManager.getSubscription().then(function(isSubbed){
                if(isSubbed != null && getCookie("isPushSubscribed") == "true"){
                    document.getElementById("pushPermission").style.display = "none";
                }
            });
        })
    }else{
        thisBrowserSupportsPush = "false";
        document.getElementById("pushChoice").style.display = "none";
        document.getElementById("editPushChoice").style.display = "none";
        document.getElementById("pushable").checked = false;
        document.getElementById("editPushable").checked = false;
        document.getElementById("pushPermission").style.display = "none";
    }
}

function updateUpgradeButton(){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var data = {"method":"checkPremium", "username":username, "authCode":authCode};
    makePostRequest("/", data, "updateUpgradeButton");
}

function handleUpdateUpgradeButtonReturn(data){
    if(data == 0){
        return;
    }
    if(data == 1){
        document.getElementById("upgrade").style.display = "none";
        document.getElementById("downgrade").style.display = "block";
    }
    if(data == 2){
        return;
    }
}

function checkIfSubbed(){
    if("serviceWorker" in navigator){
        navigator.serviceWorker.getRegistration().then(function(reg){
            reg.pushManager.getSubscription().then(function(isSubbed){
                if(isSubbed != null){
                    return(1);
                }else{return(0);}
            });
        })
    }else{return(2);}
}
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
    expireTime = currTime + 10*365*60*60*24*1000;
    expireString = (new Date(expireTime)).toUTCString();
    document.cookie = name + "=" + value +";"+"expires=" + expireString +";";
}

function makePostRequest(url, requestParams, method){
    if(method != "clearCachedRequests" && navigator.onLine){showOverlay();}
    if(navigator.onLine == false){
        cacheRequest(requestParams);
        return;
    }
    url = "/"
    $.ajax({
        type: "POST",
        url: url,
        data: requestParams,
        success: function(data){handleRequestReturn(data, method);}
    });
}

function makeGetRequest(url, requestParams, method){
    showOverlay()
    url = "/"
    $.ajax({
        type: "GET",
        url: url,
        data: requestParams,
        success: function(data){handleRequestReturn(data, method);}
    });
}

function handleRequestReturn(data, method){
    hideOverlay();
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
    if(method == "getArchived"){
        handleGetArchivedReturn(data);
    }
    if(method == "deleteTask"){
        handleDeleteTaskReturn(data);
    }
    if(method == "changePass"){
        handleChangePassReturn(data);
    }
    if(method == "updatePushable"){
        handleUpdatePushableReturn(data);
    }
    if(method == "stripeSubscribePost"){
        handleStripeSubscribePostReturn(data);
    }
    if(method == "updateUpgradeButton"){
        handleUpdateUpgradeButtonReturn(data);
    }
    if(method == "deleteCustomerPost"){
        handleDeleteCustomerPostReturn(data);
    }
    if(method == "updateSub"){
        handleUpdateSubReturn(data);
    }
}

function getAll(){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var timeOffset = timezoneOffset();
    document.getElementById("tasks").innerHTML = localStorage["lastTaskGetReturn"];
    if(navigator.onLine != true){
        return;
    }
    if(username == 0 || authCode == 0){
        openLoginBar();
    }else{
        var data = {"username":username, "authCode":authCode, "method":"getAll", "sort":"default", "archived":"false", "timeOffset":timeOffset};
        makePostRequest("/", data, "getAll");
    }
}

function handleGetAllReturn(data){
    data = escapeHTML(data);
    if(data == 0){
        openLoginBar();
    }
    if(data == 2){
        document.getElementById("tasks").innerHTML = "<div class='task' style='height:auto;'><h2 class='taskTitle'>All Done</h2></div>";
        localStorage["lastTaskGetReturn"] = document.getElementById("tasks").innerHTML;
    }
    if(data != 0 && data != 2){
        localStorage["lastTaskGetReturn"] = data;
        document.getElementById("tasks").innerHTML = data;
    }
}

function getArchived(){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var timeOffset = timezoneOffset();
    closeNav();
    if(navigator.onLine != true){
        document.getElementById("tasks").innerHTML = "<div class='task' id='infoHeader' style='height:auto;'><h2 class='taskTitle'>Archive Unavailable Offline</h2><div class='taskBody'>I'm working on it, sorry 😞 </div><input type='button' id='archivedButton' value='Go Back' onclick='getAll();'></div>";
    }
    if(username == 0 || authCode == 0){
        openLoginBar();
    }else{
        var data = {"username":username, "authCode":authCode, "method":"getAll", "sort":"createTime", "archived":"true", "timeOffset":timeOffset};
        makePostRequest("/", data, "getArchived");
    }
}

function handleGetArchivedReturn(data){
    data = escapeHTML(data);
    if(data == 0){
        openLoginBar();
        return;
    }
    if(data == 2){
        document.getElementById("tasks").innerHTML = "<div class='task' id='infoHeader' style='height:auto;'><h2 class='taskTitle'>Nothing Archived</h2><input type='button' id='archivedButton' value='Go Back' onclick='getAll();'></div>";
        localStorage["lastArchiveGetReturn"] = "";
        return;
    }
    if(data == 3){
        var infoTask = "<div class='signup' id='infoHeader' style='height:auto;'>";
        infoTask += "<div>";
        infoTask += "Oops, that's a premium feature, please <a href='upgrade.html'><b>Upgrade to Premium</b></a> to access your archive<br>"
        infoTask += "<input type='button' value='Go Back' onclick='getAll();'></input>"
        infoTask += "</div>";
        infoTask += "</div>";
        document.getElementById("tasks").innerHTML = infoTask;
        return;
    }
    if(data != 0 && data != 2 && data != 3){
        localStorage["lastArchiveGetReturn"] = data;
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
        closeLoginBar();
        updateUpgradeButton();
        getAll();
    }
    else{
        document.getElementById("loginInfo").innerHTML = "Username or password incorrect";
    }
}

function addTaskPost(title, description, dueTime, tags){
    title = escapeHTML(title);
    description = escapeHTML(description);
    tags = escapeHTML(tags);
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var pushable = "" + document.getElementById("pushable").checked;
//    if(title.includes("\"") || title.includes("\'") ||tags.includes("\"") || tags.includes("\'") || description.includes("\"") || description.includes("\'")){
//        document.getElementById("info").innerHTML = "Tasks cannot include quotation marks";
//        return;
//    }
    if(title == ""){
        document.getElementById("info").innerHTML = "Your task needs a title";
    }else{
        if(dueTime != 0){
            var data = {"method":"addTask", 
                "username":username, 
                "authCode":authCode, "dueTime":dueTime, 
                "description":description, 
                "title":title, 
                "tags":tags, 
                "pushable":pushable};
            makePostRequest("/", data, "addTaskPost");
        }
    }
}

function handleAddTaskPostReturn(data){
    if(data == 1){
        closeAdd();
        getAll();
    }else{
        openLoginBar();;
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
    if(pass == pass2 && username != "" && pass.length > 7 && username.length > 3){
        var data = {"method":"createUser", "username":username, "userPass":pass, "inviteCode":inviteCode};
        makePostRequest("/", data, "createUser");
        return;
    }
    if(pass != pass2){
        document.getElementById("info").innerHTML = "Passwords Don't Match";
        return;
    }
    if(username == "" || username.length < 4){
        document.getElementById("info").innerHTML = "Username too short";
        return;
    }
    if(pass.length < 8){
        document.getElementById("info").innerHTML = "Password must be longer than 8 characters";
        return;
    }
}

function changePass(oldPass, newPass1, newPass2){
    username = getCookie("username");
    if(newPass1 != newPass2){
        document.getElementById("changePassInfo").innerHTML = "Your Passwords don't match";
        return;
    }
    if(username == 0){
        closeChangePassBar();
        openLoginBar();
        return;
    }
    if(newPass1.length < 8){
        document.getElementById("changePassInfo").innerHTML = "New Password must be at least 8 characters long"
        return;
    }
    var data = {"method":"changePass", "username":username, "oldPass":oldPass, "newPass":newPass1}
    makePostRequest("/", data, "changePass")
}

function handleChangePassReturn(data){
    if(data == 1){
        closeChangePassBar();
        logout();
    }
    else{
        document.getElementById("changePassInfo").innerHTML = "Old Password Incorrect";
    }
}

function handleCreateUserReturn(data){
    if(data == 1){
        window.location = "index.html";
    }
    if(data == 0){
        document.getElementById("info").innerHTML = "Invite Code Incorrect";
    }
    if(data == 2){
        document.getElementById("info").innerHTML = "Username Taken";
    }
    if(data == 3){
        document.getElementById("info").innerHTML = "Password Must Be At Least 8 Characters"
    }
    if(data == 4){
        document.getElementById("info").innerHTML = "Username Must Be At Least 4 Characters"
    }
}

function completeTaskPost(id){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var done = "true";
    document.getElementById(id).style.display = "none";
    var data = {"method":"completeTask", "id":id, "username":username, "authCode":authCode, "done":done};
    window.setTimeout(function(){makePostRequest("/", data, "completeTask")}, 0);
}

function restoreTaskPost(id){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var done = "false";
    document.getElementById(id).style.display = "none";
    var taskData = getTaskDataById(id);
    var title = taskData[0];
    var dueTime = getTimeFromDateString(taskData[2]);
    var data = {"method":"completeTask", "id":id, "username":username, "authCode":authCode, "done":done, "title":title, "dueTime":dueTime};
    window.setTimeout(function(){makePostRequest("/", data, "deleteTask")}, 0);
}

function handleCompleteTaskPostReturn(data){
    if(data == 1){
        getAll();
    }
}

function deleteTask(id){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    document.getElementById(id).style.display = "none";
    var data = {"method":"deleteTask", "id":id, "username":username, "authCode":authCode};
    window.setTimeout(function(){makePostRequest("/", data, "deleteTask")}, 0);
}

function handleDeleteTaskReturn(data){
    if(data == 1){
        getArchived();
    }
}

function logout(){
    setCookie("authCode", "0");
    setCookie("username", "0");
    closeNav();
    openLoginBar();
}
function closeSidebars(){
    closeNav();
    closeAdd();
    closeEdit();
    closeCalBar();
    closeLoginBar();
    closeChangePassBar();
}
/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    if(document.getElementById("nav").style.width != "0px"){
        closeNav();
        return;
    } 
    closeSidebars();
    document.getElementById("navInfo").innerHTML = "";
    document.getElementById("searchInput").value = "";
    document.getElementById("searchInput").focus();
    if(window.screen.availWidth < 500){
        document.getElementById("nav").style.width = "100%";
    }else{
        document.getElementById("nav").style.width = "300px";
        document.getElementById("main").style.marginLeft = "300px";
    }
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav(){
    document.getElementById("nav").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
}
function openLoginBar() {
    if(document.getElementById("loginBar").style.width != "0px"){
        closeLoginBar();
        return;
    }
    closeSidebars(); 
    document.getElementById("tasks").innerHTML = "<div class='task' style='height:auto;'><h2 style='padding:auto;'>You're Logged Out</h2></div>";
    document.getElementById("username").focus();
    document.getElementById("loginInfo").innerHTML = "";
    if(window.screen.availWidth < 500){
        document.getElementById("loginBar").style.width = "100%";
    }else{
        document.getElementById("loginBar").style.width = "300px";
        document.getElementById("main").style.marginLeft = "300px";
    }
}

function openChangePassBar(){
    if(document.getElementById("changePassBar").style.width != "0px"){
        closeChangePassBar();
        return;
    }
    closeSidebars();
    document.getElementById("changePassInfo").innerHTML = "";
    document.getElementById("oldPass").value = "";
    document.getElementById("newPass1").value = "";
    document.getElementById("newPass2").value = "";
    document.getElementById("oldPass").focus();
    if(window.screen.availWidth < 500){
        document.getElementById("changePassBar").style.width = "100%";
    }else{
        document.getElementById("changePassBar").style.width = "300px";
        document.getElementById("main").style.marginLeft = "300px";
    }
}

function closeChangePassBar(){
    document.getElementById("changePassBar").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
}

function closeLoginBar(){
    document.getElementById("loginBar").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
}
function openAdd(){
    if(document.getElementById("add").style.width != "0px"){
        closeAdd();
        return;
    }
    closeSidebars();
    document.getElementById("title").value = "";
    document.getElementById("description").value = "";
    document.getElementById("tags").value = "";
    document.getElementById("info").value = "";
    document.getElementById("pushable").checked = true;
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

function openEdit(id){
    if(document.getElementById("edit").style.width != "0px" && document.getElementById("editId").innerHTML == id){
        closeEdit();
        return;
    }
    closeSidebars();
    document.getElementById("editInfo").innerHTML = "";
    if(window.screen.availWidth < 500){
        document.getElementById("edit").style.width = "100%";
        document.getElementById("editTitle").focus();
    }else{
        document.getElementById("editTitle").focus();
        document.getElementById("edit").style.width = "300px";
        document.getElementById("main").style.marginLeft = "300px";
    }
    taskData = getTaskDataById(id);
    title = taskData[0];
    description = taskData[1];
    dueTimeString = taskData[2];
    tags = taskData[3];
    updateEditFields(title, description, dueTimeString, tags, id);
}

function closeEdit(){
    document.getElementById("edit").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
    hideDatePicker("editDatePicker");
}

function updateEditFields(title, description, timeString, tags, id){
    var date = timeString.split(" ")[0]
    var time = timeString.split(" ")[1]
    document.getElementById("editTitle").value = title;
    document.getElementById("editDescription").value = description;
    document.getElementById("editDateString").value = date;
    document.getElementById("editTimeString").value = time;
    document.getElementById("editInfo").innerHTML = "";
    document.getElementById("editId").innerHTML = id;
    document.getElementById("editTags").value = tags;
    if(thisBrowserSupportsPush == "true"){
        document.getElementById("editPushable").checked = true;
    }
}

function editTaskPost(title, description, dueTime, tags){
    title = escapeHTML(title);
    description = escapeHTML(description);
    tags = escapeHTML(tags);
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var id = document.getElementById("editId").innerHTML;
    var pushable = document.getElementById("editPushable").checked + "";
//    if(title.includes("\"") || title.includes("\'") ||tags.includes("\"") || tags.includes("\'")){
//        document.getElementById("info").innerHTML = "Title and tags cannot include quotation marks";
//        return;
//    }
    if(title == ""){
        document.getElementById("editInfo").innerHTML = "Your task needs a title";
    }else{
        if(dueTime != 0){
            var data = {"method":"editTask", 
                "username":username,
                "dueTime":dueTime, 
                "authCode":authCode, 
                "id":id, 
                "description":description, 
                "title":title, 
                "tags":tags,
                "pushable":pushable};
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
        openLoginBar();
    }
}

function getTagged(tag){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var timeOffset = timezoneOffset();
    if(username == 0 || authCode == 0){
        openLoginBar();
    }else{
        var data = {"username":username, "authCode":authCode, "method":"getTagged", "sort":"default", "tag":tag, "timeOffset":timeOffset};
        makePostRequest("/", data, "getTaggedPost");
    }
}

function handleGetTaggedReturn(data){
    data = escapeHTML(data);
    if(data == 0){
        openLoginBar();
    }
    if(data == 2){
        document.getElementById("tasks").innerHTML = "<div class='task' id='infoHeader'><h2 class='taskTitle'>No tasks with that tag</h2><input type='button' id='archiveButton' value='Go Back' onclick='getAll();'></div>";
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
    var timeOffset = timezoneOffset();
    closeSidebars();
    if(searchString.length < 1){
        document.getElementById("navInfo").innerHTML = "You need to search for something!";
        return;
    }
    closeNav();
    if(username == 0 || authCode == 0){
        openLoginBar();
    }else{
        var data = {"username":username, "authCode":authCode, "method":"search", "sort":"default", "searchString":searchString, "timeOffset":timeOffset};
        makePostRequest("/", data, "search");
    }
}

function handleSearchPostReturn(data){
    data = escapeHTML(data);
    if(data == 0){
        openLoginBar();
    }
    if(data == 2){
        document.getElementById("tasks").innerHTML = "<div class='task' style='height:auto;' id='infoFooter'><h2 class='taskTitle'>No matches</h2><input type='button' id='archiveButton' value='Go Back' onclick='getAll();'></div>";
        scroll(0,0);
    }
    if(data != 0 && data != 2){
        document.getElementById("tasks").innerHTML = data;
        scroll(0,0);
    }
}

function openCalBar(){
    if(document.getElementById("calBar").style.width != "0px"){
        closeCalBar();
        return;
    }
    closeSidebars();
    var month = new Date().getMonth();
    var year = new Date().getFullYear();
    if(window.screen.availWidth < 500){
        document.getElementById("calBar").style.width = "100%";
    }else{
        document.getElementById("calBar").style.width = "300px";
        document.getElementById("main").style.marginLeft = "300px";
    }
    renderCalPost(month, year);
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeCalBar() {
    document.getElementById("calBar").style.width = "0px";
    document.getElementById("main").style.marginLeft = "0px";
}

function renderCalPost(monthInt, year){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    if(document.getElementsByClassName("dueTime").length < 1 && navigator.onLine == true){
        if(username == 0 || authCode == 0){
            openLoginBar();
        }else{
            var data = {"username":username, "authCode":authCode, "method":"getTaskDates", "sort":"default", "month":monthInt, "year":year};
            makePostRequest("/", data, "getTaskDates");
        }
    }
    else{
        dueTimeList = document.getElementsByClassName("dueTime")
        var i = 0;
        var datesString = "";
        while(i < dueTimeList.length){
            datesList = dueTimeList[i].innerHTML.split(" ")[0].split("/").slice(0, 2);
            datesString += datesList[0] + "/" + datesList[1] + "/" + year + ",";
            i += 1;
        }
        renderCal(monthInt + ";" + datesString + ";" + year);
    }
    if(navigator.onLine == true){
        var data = {"username":username, "authCode":authCode, "method":"getTaskDates", "sort":"default", "month":monthInt, "year":year};
        makePostRequest("/", data, "getTaskDates");    
    }
}

function renderCal(data){
    if(data == 0){
        openLoginBar();
        return;
    }
    else{
        var monthInt = parseInt(data.split(";")[0]);
        var datesList = data.split(";")[1].split(",");
        var year = data.split(";")[2];
        var ii = 0;
        var parsedDatesList = "";
        while(ii < datesList.length){
            day = parseInt(datesList[ii].split("/")[0]);
            month = parseInt(datesList[ii].split("/")[1])-1;
            taskYear = parseInt(datesList[ii].split("/")[2]);
            if(day < 10){
                day = "0" + day;
            }
            parsedDatesList += day+"/"+month+"/"+taskYear;
            ii += 1;
        }
    }
    var todayDate = new Date().getDate();
    if(todayDate < 10){
        todayDate = "0" + todayDate;
    }
    var thisMonth = new Date().getMonth();
    var thisYear = new Date().getFullYear();
    var todayString = todayDate + "/" + thisMonth+"/"+thisYear;
    while(monthInt > 11){
        monthInt -= 12;
        year = parseInt(year) + 1;
    }
    while(monthInt < 0){
        monthInt += 12
        year = parseInt(year) - 1;
    }
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var monthName = monthNames[monthInt];
    var firstDay = new Date(year, monthInt, 1).getDay();
    var lastDate = new Date(year, monthInt + 1, 0).getDate();
    var i = 0;
    var n = 0;
    document.getElementById("calHead").innerHTML = "<i class='fa fa-arrow-left' onclick='renderCalPost("+(monthInt-1)+","+year+");'></i>" + monthName + " " + year + "<i class='fa fa-arrow-right' onclick='renderCalPost("+(monthInt+1)+","+year+");'></i>";
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
        if(i < 10){
            currDateString = "0"+i+"/"+monthInt+"/"+year;
        }else{
            currDateString = i+"/"+monthInt+"/"+year;
        }
        if(parsedDatesList.indexOf(currDateString) >= 0 && currDateString == todayString){
            innerHTML += "<td class='dueToday' onclick='dateSearch(" + i + ", " + monthInt+","+year + ");'>" + i + "</td>";
            i += 1;
            continue;
        }
        if(parsedDatesList.indexOf(currDateString) >= 0 && currDateString != todayString){
            innerHTML += "<td class='activeDate' onclick='dateSearch(" + i + ", " + monthInt+","+year+ ");'>" + i + "</td>";
            i += 1;
            continue;
        }
        if(currDateString == todayString){
            innerHTML += "<td class='todaysDate' onclick='dateSearch(" + i + ", " + monthInt+","+year+ ");'>" + i + "</td>";
            i += 1;
            continue;
        }
        innerHTML += "<td onclick='dateSearch(" + i + ", " + monthInt+","+year+ ");'>" + i + "</td>";
        i += 1;
    }
    innerHTML += "</tr>";
    while(i <= lastDate){
        innerHTML += "<tr>";
        n = 0;
        while(n < 7 && i <= lastDate){
            if(i < 10){
                currDateString = "0"+i+"/"+monthInt+"/"+year;
            }else{
                currDateString = i+"/"+monthInt+"/"+year;
            }
            if(parsedDatesList.indexOf(currDateString) >= 0 && currDateString == todayString){
                innerHTML += "<td class='dueToday' onclick='dateSearch(" + i + ", " + monthInt +","+year+ ");'>" + i + "</td>";
                i += 1;
                n += 1;
                continue;
            }
            if(parsedDatesList.indexOf(currDateString) >= 0 && currDateString != todayString){
                innerHTML += "<td class='activeDate' onclick='dateSearch(" + i + ", " + monthInt+","+year+ ");'>" + i + "</td>";
                i += 1;
                n += 1;
                continue;
            }
            if(currDateString == todayString){
                innerHTML += "<td class='todaysDate' onclick='dateSearch(" + i + ", " + monthInt+","+year+ ");'>" + i + "</td>";
                i += 1;
                n += 1;
                continue;
            }
            innerHTML += "<td onclick='dateSearch(" + i + ", " + monthInt+","+year+ ");'>" + i + "</td>";
            n += 1;
            i += 1;
        }
        innerHTML += "</tr>";
    }
    innerHTML += "<tbody>";
    document.getElementById("calBody").innerHTML = innerHTML;
}

function dateSearch(dateInt, monthInt, year){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var timeOffset = timezoneOffset();
    closeSidebars();
    var lowerTime = new Date(year, monthInt, dateInt, 0, 0, 0, 0).getTime()
    lowerTime = lowerTime/1000;
    var upperTime = new Date(year, monthInt, dateInt+1, 0, 0, 0, 0).getTime()
    upperTime = upperTime/1000;
    if(username == 0 || authCode == 0){
        openLoginBar();
    }else{
        if(navigator.onLine == true){
            var data = {"username":username, "authCode":authCode, "method":"dateSearch", "sort":"default", "lowerTime":lowerTime, "upperTime":upperTime, "timeOffset":timeOffset};
            makePostRequest("/", data, "dateSearch");
        }else{
            offlineDateSearch(dateInt, monthInt, year);
        }
    }
}

function handleDateSearchPostReturn(data){
    data = escapeHTML(data);
    if(data == 0){
        openLoginBar();
    }
    if(data != 0 && data != 2){
        document.getElementById("tasks").innerHTML = data;
        scroll(0,0);
    }
}
function renderDatePicker(monthInt, divId, tableId, headId, inputId, year){
    document.getElementById(divId).style.display = "inline-block";
//    document.getElementById(divId).style.position = "absolute";
    document.getElementById(divId).style.height = "80%";
    while(monthInt > 11){
        monthInt -= 12;
        year = parseInt(year) + 1;
    }
    while(monthInt < 0){
        monthInt += 12
        year = parseInt(year) - 1;
    }
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var monthName = monthNames[monthInt];
    var firstDay = new Date(year, monthInt, 1).getDay();
    var lastDate = new Date(year, monthInt + 1, 0).getDate();
    var i = 0;
    var n = 0;
    var thisYear = new Date().getFullYear();
    var today = new Date().getDate();
    var thisMonth = new Date().getMonth();
    document.getElementById(headId).innerHTML = "<i class='fa fa-arrow-left' onclick='renderDatePicker("+(monthInt-1)+",\""+divId+"\",\""+tableId+"\",\""+headId+"\",\""+inputId+"\","+year+");'></i>" + monthName + " " + year + "<i class='fa fa-arrow-right' onclick='renderDatePicker(" + (monthInt+1) + ",\""+divId+"\",\""+tableId+"\",\""+headId+"\",\""+inputId+"\","+year+");'></i>";
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
        if(i == today && monthInt == thisMonth && year == thisYear){
            innerHTML += "<td class='todaysDate' onclick='updateDateInput(\""+inputId+"\","+i+","+(monthInt+1)+",\""+year+"\");'>" + i + "</td>"; 
        }else{
            innerHTML += "<td onclick='updateDateInput(\""+inputId+"\","+i+","+(monthInt+1)+",\""+year+"\");'>" + i + "</td>";
        }
        i += 1;
    }
    innerHTML += "</tr>";
    while(i <= lastDate){
        innerHTML += "<tr>";
        n = 0;
        while(n < 7 && i <= lastDate){    
            if(i == today && monthInt == thisMonth && year == thisYear){
                innerHTML += "<td class='todaysDate' onclick='updateDateInput(\""+inputId+"\","+i+","+(monthInt+1)+",\""+year+"\");'>" + i + "</td>"; 
            }else{
                innerHTML += "<td onclick='updateDateInput(\""+inputId+"\","+i+","+(monthInt+1)+",\""+year+"\");'>" + i + "</td>";
            }
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

function subscribe(){
        navigator.serviceWorker.getRegistration().then(function(reg){
            reg.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: base64UrlToUint8Array("BIceeej1Sv37OVW0Ey4miAkZ4ZYxEQOwp4iNJa6s-MjdvjMJjV6Z9XVZ2i0eRscywzDhDSWgf-3i974Y4qAnpKs")
            }).then(function(subInfo){
                updateSubInfo(subInfo);
            });
        }).catch(function(err){console.log(err);})
        setCookie("pnSubbed", "true");
        document.getElementById("pushPermission").style.display = "none";
}

function base64UrlToUint8Array(base64UrlData) {
    const padding = '='.repeat((4 - base64UrlData.length % 4) % 4);
    const base64 = (base64UrlData + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');
    const rawData = window.atob(base64);
    const buffer = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
        buffer[i] = rawData.charCodeAt(i);
    }
    return buffer;
}

function updateSubInfo(subInfo){
    username = getCookie("username");
    authCode = getCookie("authCode");
    var data = {"method":"updateSub", "username":username, "authCode":authCode, "subInfo":JSON.stringify(subInfo)};
    makePostRequest("/", data, "updateSub");
    console.log("Sub Info Updated");
}

function updatePushable(createTime){
    username = getCookie("username");
    authCode = getCookie("authCode");
    var data = {"method":"updatePushable", "username":username, "authCode":authCode, "createTime":createTime};
    makePostRequest("/", data, "updatePushable");
}

function handleUpdatePushableReturn(data){
    getAll();
}

Date.prototype.stdTimezoneOffset = function() {
    var jan = new Date(this.getFullYear(), 0, 1);
    var jul = new Date(this.getFullYear(), 6, 1);
    return Math.max(jan.getTimezoneOffset(), jul.getTimezoneOffset());
}

Date.prototype.dst = function() {
    return this.getTimezoneOffset() < this.stdTimezoneOffset();
}

function timezoneOffset(){
    offset = new Date().getTimezoneOffset() * 60;
//    if(!(new Date().dst())){
//        offset += 60*60;
//    }
    return offset;
}

function showOverlay(){
    document.getElementById("overlay").style.display = "block";
}
function hideOverlay(){
    document.getElementById("overlay").style.display = "none";
}
function escapeHTML(unsafe) {
    unsafe = unsafe
//    .replace(/&/g, "&amp;")
//    .replace(/</g, "&lt;")
//    .replace(/>/g, "&gt;")
//    .replace(/"/g, "\"")
//    .replace(/'/g, "&#039;");
    return(unsafe);
}

function getTaskDataById(id){
    var taskDiv = document.getElementById(id);
    var taskChildNodes = taskDiv.childNodes;
    var title = taskChildNodes[0].innerHTML;
    var description = taskChildNodes[1].innerHTML;
    if(description == "<span class=\"italic\">No details</span>"){description = "";}
    var dueTimeAndTaskTagsWrapper = taskChildNodes[2];
    var dueTime = dueTimeAndTaskTagsWrapper.childNodes[0].innerHTML;
    var taskTags = dueTimeAndTaskTagsWrapper.childNodes[1];
    var tags = "";
    for(var i = 0; i < taskTags.childNodes.length; i++){
        tags += taskTags.childNodes[i].innerHTML + ",";
    }
    if(tags == "<span class=\"italic\">No tags</span>,"){tags = "";}
    return([title, description, dueTime, tags, id]);
}

function getTimeFromDateString(dateString){
    date = dateString.split(" ")[0];
    dateList = date.split("/");
    day = parseInt(dateList[0]);
    month = parseInt(dateList[1]);
    year = parseInt(dateList[2]);
    time = dateString.split(" ")[1];
    timeList = time.split(":");
    hour = timeList[0];
    minute = timeList[1];
    time = new Date(year,month-1,day,hour,minute,0,0).getTime();
    time = time/1000;
//    console.log(time);
    return(time);
}

function stripeSubscribePost(token){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var id = token.id;
    var email = token.email;
    var data = {"method":"createCustomer", "token":id, "username":username, "authCode":authCode, "email":email};
    console.log(data);
    makePostRequest("/", data, "stripeSubscribePost");
    return(false);
}

function handleStripeSubscribePostReturn(data){
    console.log(data);
    if(data == 1){
        window.location = "/";
        return;
    }
    if(data == 2){
        document.getElementById("premiumInfo").innerHTML = "You're already a subscriber, thanks 😄 ! If you don't already have access to premium features, please contact admin@cuntoir.com <br>";
        document.getElementById("premiumInfo").innerHTML += "<input type='button' onclick='window.location=\"/\";' value='Go Back'></input>";
        return;
    }
    if(data == 0){
        document.getElementById("premiumInfo").innerHTML = "You're not logged in, sorry. Please <a href='/'>Log In</a> and try again.";
        return;
    }
    if(data == 4){
        document.getElementById("premiumInfo").innerHTML = "Sorry, something went wrong on our end. If this problem persists, please contatct admin@cuntoir.com";
        return;
    }
    else{
        data = "Sorry, your card was declined. The message we got from Stripe was: \"" + data + "\"<br>";
        data += "<input type='button' onclick='window.location=\"/\";' value='Go Back'></input>";
        document.getElementById("premiumInfo").innerHTML = data;
        return;
    }
}
function deleteCustomerPost(){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    var data = {"method":"clientDeleteCustomer", "username":username, "authCode":authCode};
    makePostRequest("/", data, "deleteCustomerPost");
}

function handleDeleteCustomerPostReturn(data){
    console.log(data)
    if(data == 1){
        setCookie("isPushSubscribed", "false");
        updateSubButton();
        updateUpgradeButton();
        closeSidebars();
        getAll();
        return;
    }
    if(data == 0){
        logout();
        return;
    }
    if(data == 2){
        document.getElementById("navInfo").innerHTML = "You never were subscribed";
    }
}

function handleUpdateSubReturn(data){
    closeSidebars();
    if(data == 3){
        updateSubButton()
        var infoTask = "<div class='signup' id='infoHeader' style='height:auto;'>";
        infoTask += "<div>";
        infoTask += "Oops, notifications are a premium feature, please <a href='upgrade.html'><b>Upgrade to Premium</b></a> to get them<br>"
        infoTask += "<input type='button' value='Go Back' onclick='getAll();'></input>"
        infoTask += "</div>";
        infoTask += "</div>";
        document.getElementById("tasks").innerHTML = infoTask;
        return;
    }
    if(data == 0){
        logout();
    }
    if(data == 1){
        var d = new Date();
        d.setTime(d.getTime() + (1000*356*24*60*60*1000));
        var expires = d.toUTCString();
        setCookie("isPushSubscribed", "true")
    }
}

function cacheRequest(data){
    var dataString = JSON.stringify(data);
    var currentNumberOfDuePosts = parseInt(localStorage["duePosts"])
    localStorage["duePost" + (currentNumberOfDuePosts + 1)] = dataString;
    localStorage["duePosts"] = (currentNumberOfDuePosts + 1);
    fakePostRequest(data, currentNumberOfDuePosts + 1);
}

function clearCachedRequests(){
    var duePostCount = parseInt(localStorage["duePosts"]);
    if(navigator.onLine == true && duePostCount > 0){
    var i = 0;
    while(i < duePostCount){
        var data = JSON.parse(localStorage["duePost" + (i+1)]);
        localStorage.removeItem("duePost" + (i+1));
        console.log(data);
        makePostRequest("/", data, "clearCachedRequests")
        i = i + 1;
    }
    localStorage["duePosts"] = 0;
    console.log(userBusy());
    getAll();
    }
}

function userBusy(){
    var sideBars = document.getElementsByClassName("sidebar");
    var i = 0;
    while(i < sideBars.length){
        if(sideBars[i].style.width != "0px"){return true;}
        i += 1;
    }
    return false;
}
function fakePostRequest(data, postNumber){
    console.log(data);
    if(data["method"] == "addTask"){
        fakeAddTask(data, postNumber);
    }
}
function fakeAddTask(data, id){
    var title = data["title"];
    var description = data["description"];
    if(description.length == 0){
        description = "<span class='italic'>No details</span>";
    }
    var dueTime = data["dueTime"] * 1000;
    var timeOffset = new Date().getTimezoneOffset();
    var tags = data["tags"];
    var idString = "duePost" + id + "";
    var dueYear = new Date(dueTime - timeOffset).getFullYear();
    var dueMonth = new Date(dueTime - timeOffset).getMonth() + 1;
    var dueDay = new Date(dueTime - timeOffset).getDate();
    var dueHour = new Date(dueTime - timeOffset).getHours() + 1;
    var dueMinute = new Date(dueTime - timeOffset).getMinutes() + 1;
    var dueString  = dueDay + "/" + dueMonth + "/" + dueYear + " " + dueHour + ":" + dueMinute;
    var taskString = "<div class='task' id='"+id+"'><h2 class='taskTitle'>"+title+"</h2>";
    taskString += "<div class='taskBody'>" + description + "</div>";
    taskString += "<div class='tagAndDueTimeWrapper'>";
    taskString += "<div class='dueTime' onclick='dateSearch("+dueDay+","+(dueMonth-1)+","+dueYear+")'>"+dueString+"</div>";
    taskString += "<div class='taskTags'>";
    var i = 0;
    while(i < tags.split(",").length){
        if(tags.split(",")[i].length == 0){i+=1;continue;}
        taskString += "<span class='taskTag' onclick='getTagged(\""+tags.split(",")[i]+"\")'>"+tags.split(",")[i]+"</span>";
        i += 1;
    }
    if(tags.length < 1){
        taskString += "<span class='noTaskTag'><span class='italic'>No tags</span></span>";
    }
    taskString += "</div>";
    taskString += "</div>";
    taskString += "<button type='button' class='archiveButton' onclick='fakeDeleteTask(" + id + ");'><i class='fa fa-times' aria-hidden='true'></i></button>";
    taskString += "</div>";
    document.getElementById("tasks").innerHTML = taskString + document.getElementById("tasks").innerHTML;
    localStorage["lastTaskGetReturn"] = document.getElementById("tasks").innerHTML;
    closeSidebars();
    getAll();
}

function fakeDeleteTask(id){
    var postString = "duePost" + id;
    var taskString = "<div class=\"task\" id=\""+id+"\">"+document.getElementById(id).innerHTML+"</div>";
    document.getElementById(id).style.display = "none";
    var oldLastTaskGetReturn = localStorage.getItem("lastTaskGetReturn");
    var newLastTaskGetReturn = oldLastTaskGetReturn.replace(taskString, "");
    localStorage.setItem("lastTaskGetReturn", newLastTaskGetReturn);
    localStorage.removeItem(postString);
    localStorage["duePosts"] = parseInt(localStorage["duePosts"]) - 1;
    getAll();
}

function offlineDateSearch(day, month, year){
    month = month + 1;
    if(day < 10){
        day = "0" + day;
    }
    if(month < 10){
        month = "0" + month;
    }
    var dateString = day + "/" + month + "/" + year;
    var tasks = document.getElementsByClassName("task");
    var i = 0;
    var infoString = "<div class='task' id='infoHeader' style='height:auto;width:auto;'><h2 class='taskTitle'>Tasks on "+dateString+"</h2></div>";
    var returnString = infoString;
    console.log(dateString);
    while(i < tasks.length){
        var task = tasks[i];
        var taskString = "<div class=\"task\" id=\""+task.id+"\">" + task.innerHTML + "</div>";
        var tagAndDueTimeWrapper = task.children[2];
        var dueTimeNode = tagAndDueTimeWrapper.children[0]
        var dueTimeString = dueTimeNode.innerHTML.split(" ")[0];
        console.log(dueTimeString);
        if(dateString == dueTimeString){
            returnString += taskString;
        }
        i += 1;
    }
    if(returnString != infoString){
        returnString += "<div class='task' id='infoFooter' style='height:auto;'><input type='button' id='archiveButton' onclick='getAll();' value='Go Back'></div>";
        document.getElementById("tasks").innerHTML = returnString;
    }else{
        returnString += "<div class='task' style='height:auto;'><h2 class='taskTitle'>No tasks</h2></div>"
        returnString += "<div class='task' id='infoFooter' style='height:auto;'><input type='button' id='archiveButton' onclick='getAll();' value='Go Back'></div>";
        document.getElementById("tasks").innerHTML = returnString;
    }
}
