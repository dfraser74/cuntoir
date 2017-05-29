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
        document.getElementById("tasks").innerHTML = "<div id='task'><h2 id='taskTitle'>You're all done, congrats!!</h2></div>";
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

function addTaskPost(title, description, dueTime){
    var username = getCookie("username");
    var authCode = getCookie("authCode");
    if(title == ""){
        document.getElementById("info").innerHTML = "Your task needs a title";
        return;
    }
    if(dueTime == 0){return}
    var data = {"method":"addTask", "username":username, "authCode":authCode, "dueTime":dueTime, "description":description, "title":title};
    makePostRequest("/", data, "addTaskPost");
}

function handleAddTaskPostReturn(data){
    if(data == 1){
        window.location = "index.html";
    }else{
        window.location = "login.html";
    }
}

function addTaskGet(){
    window.location = "addTask.html"
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
        console.log(data);
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
