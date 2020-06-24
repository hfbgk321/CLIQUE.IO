// const notBubbleUp = require("extra").notBubbleUp;
// console.log('1');

console.log(closeNotifButt);
function notBubbleUp2(e) {
  // window.location = "{%url 'delete_notification' notification.id%}";
  e.stopImmediatePropagation();
}
console.log(document.cookie);
function navbarDrop() {
  // if(document.getElementById('navbar-toggler').getAttribute('aria-expanded')=='true'){
  // document.getElementById('navbar-toggler').setAttribute("aria-expanded","false");
  // document.getElementById('navbar-toggler').classList.add("collapsed");
  // }
  // else if(document.getElementById('navbar-toggler').getAttribute('aria-expanded')=='false'){
  //     document.getElementById('navbar-toggler').setAttribute('aria-expanded','true');
  //     document.getElementById('navbar-toggler').classList.remove("collapsed");
  // }
  // document.getElementById("navbar-toggler").setAttribute("aria-expanded","false");
  if (
    document.getElementById("navbarSupportedContent").className ==
      "navbar-collapse collapse show" ||
    document.getElementById("navbarSupportedContent").className ==
      "navbar-collapse collapsing"
  ) {
    document.getElementById("navbarSupportedContent").className =
      "collapse navbar-collapse";
    var x = document.querySelectorAll(".nav-link");
    for (var i = 0; i < x.length; i++) {
      x[i].style.marginBottom = "0px";
    }
  } else {
    console.log("hello");
    document.getElementById("navbarSupportedContent").className =
      "navbar-collapse collapse show";
    var x = document.querySelectorAll(".nav-link");
    for (var i = 0; i < x.length; i++) {
      x[i].style.marginBottom = "10px";
    }
  }
}
function passFriendsIDToInput(friendID){
    document.getElementById("friendID").value=friendID;
    console.log(document.getElementById("friendID").value);
}
function closeFriendsList() {
  document.getElementById("friendsList").style.display = "none";
}


function submit1() {
    console.log("hey");
    var appForm = document.querySelector("#application-form");
    console.log(appForm);
    appForm.classList.remove("hideform");
    appForm.classList.add("showform");
}

function closeAppForm() {
  // let x = document.getElementById("application-form");
  // x.style.display = "none";
  var element = document.getElementById("application-form");
  element.classList.add("hideform");
  element.classList.remove("showform");
  // var element2 = document.getElementById("overlay2");
  // element2.classList.add("hidden");
  // element2.classList.remove("show1");
}

function startChat(userID) {
  document.getElementById("chatBox").style.display = "block";
  document.getElementById("friendsList").style.display = "none";
}
function openFriendsList() {
  document.getElementById("friendsList").style.display = "block";
}
function endChat() {
  document.getElementById("chatBox").style.display = "none";
}
function saveURL() {
  document.cookie = "deleteNotification=true";
  if (window.location.href.indexOf("posts") != -1) {
    document.cookie =
      "currentPage=" +
      window.location.href.substring(window.location.href.indexOf("posts"));
  }
}
function setSavedPage() {
  if (document.cookie.indexOf("deleteNotification=true") != -1) {
    document.getElementById("savePage").value = document.cookie.substring(
      document.cookie.indexOf("posts"),
      document.cookie.indexOf(";", document.cookie.indexOf("posts"))
    );

    document.cookie = "deleteNotification=false";
  }
}
function showNotifications() {
  document.cookie = "notificationClicked=on";

  var box = document.getElementById("notification-box");

  //
  // box.classList.add("show2");
  // }
  // else{
  //     box.classList.remove("show2");
  //     box.classList.add("hide1");
  // }
  if (box.classList.contains("hide1")) {
    box.classList.remove("hide1");
  }
  box.classList.add("show2");
}
function hideNotifications() {
  var box = document.getElementById("notification-box");
  document.cookie = "notificationClicked=off";

  if (box.classList.contains("show2")) {
    box.classList.remove("show2");
  }
  box.classList.add("hide1");
}
