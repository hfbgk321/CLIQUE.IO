// const notBubbleUp = require("extra").notBubbleUp;
// console.log('1');

// function addQuestion(){
//   var input = document.createElement("INPUT");
//   input.setAttribute('class','popupquestion');
//   input.setAttribute("placeholder", "Ex: What skills can you bring to this project?");
//   document.querySelector("#q-div").appendChild(document.createElement("BR"));
//   document.querySelector("#q-div").appendChild(document.createElement("BR"));
//   document.querySelector("#q-div").appendChild(document.createElement("BR"));
//   document.querySelector("#q-div").appendChild(document.createElement("BR"));
//   document.querySelector("#q-div").appendChild(document.createElement("BR"));
//   document.querySelector("#q-div").appendChild(input);
//   var delbtn = document.createElement("BUTTON");
//   delbtn.setAttribute("class", "close-button-q");
//   delbtn.innerHTML = "&times";
//   delbtn.setAttribute("onclick", "removeQuestion();");
//   document.querySelector("#q-div").appendChild(delbtn);
// }


function addQuestion() {
  var newdiv = document.createElement("div");
  var input = document.createElement("INPUT");
  newdiv.setAttribute('id','additionalQuestion');
 
  input.setAttribute('class','popupquestion');
  input.setAttribute("placeholder", "Ex: What skills can you bring to this project?");
  newdiv.appendChild(input);

  // var delbtn = document.createElement("a");
  // delbtn.setAttribute("class", "close-button-q");
  // delbtn.innerHTML = "&times";
 
  // delbtn.setAttribute("onclick", "removeQuestion();");

  // newdiv.appendChild(delbtn);
  newdiv.setAttribute("class", "child");

  var deleteButton=(document.createElement('a'));
  deleteButton.setAttribute("class","close-button-q");
  deleteButton.innerHTML="&times";
  deleteButton.setAttribute('id','additionalQ');
  // deleteButton.setAttribute("onclick","removeQ(this.id)");
  deleteButton.setAttribute("onclick","removethis(this)");
  additionalQuestionIndex++;
  newdiv.appendChild(deleteButton);

  document.querySelector("#q-div").appendChild(newdiv);
 
 
}
function removethis(input){
  input.parentNode.remove();
}
function saveFilters(){
  var keyWord=document.getElementById('search').value;
  document.cookie='filterSearch='+keyWord;
  // var interests=document.querySelectorAll('input[type="checkbox"]:not([checked=false])');
  var interests=document.querySelectorAll('#interest');
  var checkedInterests="";
  for(var i =0;i<interests.length;i++){
      if(interests[i].checked){
        checkedInterests+=interests[i].value+",";
      }
  }
  var sortByChecks=''
  document.cookie='checkedInterests='+checkedInterests;
  var sortBy=document.querySelectorAll('#sortBy');
  for(var i=0;i<sortBy.length;i++){
    if(sortBy[i].checked){
        sortByChecks+=sortBy[i].value;
    }
  }
  document.cookie='sortByChecks='+sortByChecks;
}
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
// function removeQuestion(){
//   var q_div = document.querySelector(".q-div");
//   var lst = document.querySelectorAll(".child");
//   console.log(lst);
//   console.log(lst.length-1);
//   var node = lst[lst.length-1];
//   console.log(node);
//   q_div.removeChild(node);
//   q_div.removeChild(q_div.lastChild);
  
// }

// function removeQ(questID){
//   var id=questID.substring(11);
//   console.log(id);
//   console.log(document.getElementById('additionalQuestion'+id));
//   document.getElementById('additionalQuestion'+id).remove();
// }
// function selectSortBy(input) {
//   console.log('pressed');
//   var boxes=document.querySelectorAll('#sortBy');
//   for(var i=0;i<boxes.length;i++){
//     boxes[i].checked=false;
//   }
//   if(!input.checked){
//     input.checked=true;
//   }
// }
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

function viewApp(){
  console.log(document.querySelector("#viewAppBox"));
  document.querySelector("#viewAppBox").classList.remove("viewAppHide");
  document.querySelector("#viewAppBox").classList.add("viewAppShow");
  var element2 = document.getElementById("overlay2");
  element2.classList.add("show1");
  element2.classList.remove("hidden");
}

function closeApp(){
  console.log("hey");
  document.querySelector("#viewAppBox").classList.remove("viewAppShow");
  document.querySelector("#viewAppBox").classList.add("viewAppHide");
  var element2 = document.getElementById("overlay2");
  element2.classList.add("hidden");
  element2.classList.remove("show1");
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
  // event.preventDefault();
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
  // event.preventDefault();
  var box = document.getElementById("notification-box");
  document.cookie = "notificationClicked=off";
  if (box.classList.contains("show2")) {
    box.classList.remove("show2");
  }
  box.classList.add("hide1");
}
function showFriendsList(){
  
}
function hideFriendsList(){

}