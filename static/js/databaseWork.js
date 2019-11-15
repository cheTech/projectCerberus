var daysofweek = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"];
var xhr = new XMLHttpRequest();
xhr.open("GET", "/api/getGroups", false);
xhr.send();
data = JSON.parse(xhr.responseText);
if (xhr.status == 200){
    if (data["status"] == "ok") {
        var Groups = data["items"];
    } else {
        bootstrap_alert.warning("Произошла ошибка при получении списка групп '" + data["error"]["reason"] + "'");
    }
} else {
    bootstrap_alert.warning("Произошла ошибка при получении списка групп '" + xhr.status + "'");
}

xhr.open("GET", "/api/getUsers", false);
xhr.send();
data = JSON.parse(xhr.responseText);
if (xhr.status == 200){
    if (data["status"] == "ok") {
        var Users = data["items"];
    } else {
        bootstrap_alert.warning("Произошла ошибка при получении списка пользователей '" + data["error"]["reason"] + "'");
    }
} else {
    bootstrap_alert.warning("Произошла ошибка при получении списка пользователей '" + xhr.status + "'");
}

var Teachers = [];
for (i=1;i<Users.length;i++){
    user = Users[i];
    if(Groups[user["groupid"]]["ownerid"]===0){
        Teachers.push(user);
    }
}

ModalSelectUser = function() {
    htmlcont = '<div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true" id="alert-modal"> <div class="modal-dialog" role="document"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal" aria-label="Закрыть"> <span aria-hidden="true">&times;</span> </button> </div> <div class="modal-body"> <table class="table"> <thead> <tr> <th scope="col">Номер</th> <th scope="col">Имя</th> <th scope="col">Префикс</th> <th scope="col"> </th></tr> </thead> <tbody>';
    for(i=0;i<Teachers.length;i++){
        htmlcont += '<tr> <th scope="row">';
        htmlcont += Teachers[i]["id"];
        htmlcont += '</th> <td>';
        htmlcont += Teachers[i]["name"];
        htmlcont += '</td> <td>';
        htmlcont += Teachers[i]["pref"];
        htmlcont += '</td> <td>';
        htmlcont += '<button class="btn btn-secondary" onclick="setOwnerID(' + Teachers[i]["id"] + ')">Выбрать</button>';
        htmlcont += '</td> </tr>';
    }
    htmlcont += ' </tbody> </table> </div> <div class="modal-footer"> <button type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button> </div> </div> </div></div>';
    $("#modal-window").html(htmlcont);
    $("#alert-modal").modal("show");
}
setOwnerID = function(userid){
    $("#ownerid-in").val(userid);
    $("#selected-user").html("Выбран пользователь: <b>"+Users[userid]["name"]+"</b>.");
    $("#alert-modal").modal('toggle');
}

var timeResfresh = function() {
    htmlcont = "";
    kvantVal = $("#kvant-in").val();
    dayVal = $("#day-in").val();
    matchGroups = $.grep(Groups, function(n, i) {
        return n.kvant === kvantVal & n.dayofweek === parseInt(dayVal);
    });
    if (matchGroups.length == 0) {
        htmlcont += "<option value='-1'>Групп в этот день не найдено!</option>";
    } else {
        htmlcont += "<option>Выберите время</option>";
    }
    for (i = 0; i < matchGroups.length; i++) {
        group = matchGroups[i];
        htmlcont += "<option value='" + group["id"] + "'>" + group["time"] + " (Наставник: " + Users[group["ownerid"]]["name"] + ")</option>";
    }
    $("#time-in").html(htmlcont);
}

db = function(){}
db.deleteUser = function(userid) {
    requestData = JSON.stringify({
        userid:userid
    });

    xhr.open("POST", "/api/deleteUser", false);
    xhr.send(requestData);
    if(xhr.status == 200){
        data = JSON.parse(xhr.responseText);
        if (data["status"] == "ok") {
            bootstrap_alert.warning("Пользователь " + userid + " успешно удален!"); 
        } else {
            bootstrap_alert.warning("Произошла ошибка при удалении " + data["error"]["reason"]);
        }
    } else {
        bootstrap_alert.warning("Произошла ошибка при удалении " + xhr.status);
    }
}
db.deleteGroup = function(groupid) {
    requestData = JSON.stringify({
        groupid:groupid
    });

    xhr.open("POST", "/api/deleteGroup", false);
    xhr.send(requestData);
    if(xhr.status == 200){
        data = JSON.parse(xhr.responseText);
        if (data["status"] == "ok") {
            bootstrap_alert.warning("Группа " + groupid + " успешно удалена!"); 
        } else {
            bootstrap_alert.warning("Произошла ошибка при удалении " + data["error"]["reason"]);
        }
    } else {
        bootstrap_alert.warning("Произошла ошибка при удалении " + xhr.status);
    }
}

db.addGroup = function(time,ownerid,dayofweek,cab){
    requestData = JSON.stringify({
        ownerid:ownerid,
        time:time,
        dayofweek:dayofweek,
        kvant:Groups[Users[ownerid]["groupid"]]["kvant"],
        cab:cab
    });
    xhr.open("POST", "/api/addGroup", false);
    xhr.send(requestData);
    if (xhr.status == 200){
        data = JSON.parse(xhr.responseText);
        if (data["status"] == "ok") {
            bootstrap_alert.warning("Добавление группы в базу прошло успешно!");
        } else {
            bootstrap_alert.warning("Произошла ошибка при добавлении группы в базу '" + data["error"]["reason"] + "'");
        }
    } else {
        bootstrap_alert.warning("Произошла ошибка при добавлении группы в базу '" + xhr.status + "'");
    }
}
db.addUser = function(name,surname,groupid,photo){
    requestData = JSON.stringify({
        name: name,
        surname: surname,
        groupid: groupid,
        photo: photo
    });
    xhr.open("POST", "/api/addUser", false);
    xhr.send(requestData);
    if (xhr.status == 200){
        data = JSON.parse(xhr.responseText);
        if (data["status"] == "ok") {
            bootstrap_alert.warning("Добавление пользователя в базу прошло успешно!");
        } else {
            bootstrap_alert.warning("Произошла ошибка при добавлении пользователя в базу '" + data["error"]["reason"] + "'");
        }
    } else {
        bootstrap_alert.warning("Произошла ошибка при добавлении пользователя в базу '" + xhr.status + "'");
    }

}

db.changeGroup = function(groupid,time,ownerid,dayofweek,cab){
    requestData = JSON.stringify({
        groupid: groupid,
        time:time,
        ownerid:ownerid,
        dayofweek:dayofweek,
        cab:cab
    });
    xhr.open("POST", "/api/changeGroup", false);
    xhr.send(requestData);
    if (xhr.status == 200){
        data = JSON.parse(xhr.responseText);
        if (data["status"] == "ok") {
            bootstrap_alert.warning("Изменение данных группы прошло успешно!");
        } else {
            bootstrap_alert.warning("Произошла ошибка при изменении данных группы '" + data["error"]["reason"] + "'");
        }
    } else {
        bootstrap_alert.warning("Произошла ошибка при изменении данных группы '" + xhr.status + "'");
    }
}
db.changeUser = function(userid,name,surname,groupid,pref){
    requestData = JSON.stringify({
        userid:userid,
        name:name,
        surname:surname,
        groupid:groupid,
        pref:pref
    });
    xhr.open("POST", "/api/changeUser", false);
    xhr.send(requestData);
    if (xhr.status == 200){
        data = JSON.parse(xhr.responseText);
        if (data["status"] == "ok") {
            bootstrap_alert.warning("Изменение данных пользователя прошло успешно!");
        } else {
            bootstrap_alert.warning("Произошла ошибка при изменении данных пользователя '" + data["error"]["reason"] + "'");
        }
    } else {
        bootstrap_alert.warning("Произошла ошибка при изменении данных пользователя '" + xhr.status + "'");
    }
}
