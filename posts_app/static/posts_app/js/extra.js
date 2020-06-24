// document.querySelector(".close-button").adEventListener("click", function(){
//   alert("clicked");
// });
// document.getElementById("acceptedPostID").value=currentPostID;
// module.exports.notBubbleUp = notBubbleUp();
// let backButton = document.querySelector(".BackToFriend")
var condition = false;
var condition1 = false;
console.log(1);

// console.log(document.querySelectorAll('.friendID'));
// var friendsList=document.querySelectorAll('.friendID');
// for(var i =0;i<friendsList.length;i++){
//   // console.log(i);
//   friendsList[i].setAttribute('data-index', i);
//   // console.log(friendsList[i].index + 'Ye');
//   //  console.log(friendsList[i].getElementsByClassName("friendID").value);
// }
// console.log(friendsList[10]);
// console.log(friendsList[10].index);



function openInterestFilter() {
  if (condition == true) {
    const interest2 = document.getElementById("interest");
    interest2.style.display = "none";
    interest2.style.visibility = "hidden";
    condition = false;
  } else {
    const interest2 = document.getElementById("interest");
    interest2.style.display = "block";
    interest2.style.visibility = "visible";
    condition = true;
  }
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

function openLocationFilter() {
  if (condition1 == true) {
    const interest2 = document.getElementById("location1");
    interest2.style.display = "none";
    interest2.style.visibility = "hidden";
    condition1 = false;
  } else {
    const interest2 = document.getElementById("location1");
    interest2.style.display = "block";
    interest2.style.visibility = "visible";
    condition1 = true;
  }
}
function openAppDeadline() {
  if (condition1 == true) {
    const interest2 = document.getElementById("appdead");
    interest2.style.display = "none";
    interest2.style.visibility = "hidden";
    condition1 = false;
  } else {
    const interest2 = document.getElementById("appdead");
    interest2.style.display = "block";
    interest2.style.visibility = "visible";
    condition1 = true;
  }
}
function openCollegeList() {
  if (condition1 == true) {
    const interest2 = document.getElementById("college");
    interest2.style.display = "none";
    interest2.style.visibility = "hidden";
    condition1 = false;
  } else {
    const interest2 = document.getElementById("college");
    interest2.style.display = "block";
    interest2.style.visibility = "visible";
    condition1 = true;
  }
}
// filter_interest.addEventListener("click", function() {
//   );

function addGenre() {
  if (
    !document.getElementById("genreList").value == "" &&
    document
      .getElementById("genres")
      .value.indexOf(document.getElementById("genreList").value) == -1
  ) {
    document.getElementById("genres").value +=
      document.getElementById("genreList").value + ",";
  }
}

function backToFriendList() {
  openFriendsList();
}
let profileSelect = document.querySelector("#img");
// console.log(profileSelect);
let custBut = document.querySelector(".selectImg");
let filename = document.querySelector(".imgName");
let scrollnews = document.querySelector(".scrollnews");
let contentUL = document.querySelector(".news");
function selectImgName() {
  if (profileSelect.value) {
    filename.style.display = "block";
    filename.innerHTML = "" + profileSelect.value.replace(/^.*[\\\/]/, "");
    // console.log(filename.innerHTML);
    // console.log('xx');
    // filename.style.display = 'block';
  }
}
// console.log(contentUL.scrollTop);
// let Scrolltop = 0;
// console.log(1);
function scrolldown() {
  if (contentUL.scrollTop === 0) {
    contentUL.scrollTop += 256;
  } else {
    contentUL.scrollTop += 182;
  }
}

// contentUL.scrollTop = contentUL.scrollTop + '100';
// console.log(Scrolltop);

function active() {
  profileSelect.click();
}

const email = document.querySelector("#emailBox");
const universitySec = document.querySelector(".universitySec");
const universityBox = document.querySelector("#universityBox");
const majorSec = document.querySelector(".majorSec");
const majorBox = document.querySelector("#majorBox");
const emailSec = document.querySelector(".emailSec");
const BioSec = document.querySelector(".BioSec");
const BioBox = document.querySelector("#bio");
console.log(BioBox);
let box = [email, universityBox, majorBox, BioBox];
let sec = [emailSec, universitySec, majorSec, BioSec];
for (let i = 0; i < sec.length; i++) {
  sec[i].onmouseenter = function () {
    box[i].style.backgroundColor = "white";
    console.log("enter");
  };
  sec[i].onmousleave = function () {
    box[i].style.backgroundColor = "transparent";
  };
}
emailSec.onclick = function () {
  email.focus();
};
universitySec.onclick = function () {
  universityBox.focus();
};
majorSec.onclick = function () {
  majorBox.focus();
};
BioSec.onclick = function () {
  BioBox.focus();
};

document.getElementById("acceptedPostID").value;
var alertMessa = document.querySelector("#alertMessa");
console.log(alertMessa);
setTimeout(function () {
  alertMessa.display = "none";
}, 3000);

if (document.getElementById("listProjName").innerHTML == "") {
  document.getElementById("applicantList").style.display = "none";
  document.getElementById("noApplicantText").style.display = "none";
}
var index = -1;
function incrementIndex() {
  index++;
  console.log(index);
}
function fillStar() {
  stars[index].style.color = "yellow";
}
let lissss = document.querySelectorAll(".item");
console.log(lissss);
// function selectedTab(a) {
//   let lis = document.querySelectorAll('.item');
// }

const clear_button = document.querySelector(".hvr-underline-reveal");
const lst = document.querySelectorAll(".boxes");
const college = document.querySelector("#university");
function clearAll() {
  const lst = document.querySelectorAll(".boxes");
  const college = document.querySelector("#university");
  console.log(lst);
  for (let i = 0; i < lst.length; i++) {
    lst[i].checked = false;
  }
  college.value = "";
}

// var lis = document.querySelector('.features');
// var gallery = document.querySelectorAll('.gallery');
// lis.children[0].style.textDecoration = 'underline';
// for (let i = 0; i < lis.children.length; i++){
//   lis.children[i].addEventListener('click', function () {
//     for (let j = 0; j < lis.children.length; j++){
//       gallery[j].style.display = 'none';
//       lis.children[j].style.textDecoration = 'none';
//     }
//     // if (this == lis.children[1]) {
//     //   console.log(1);
//     //   var applybutton = document.querySelector('.button');
//     //   applybutton.style.display = 'none';
//     // } else {
//     //   applybutton.style.display = block';
//     // }
//     lis.children[i].style.textDecoration = 'underline';
//     gallery[i].style.display = 'block';
//   })
// }

if (document.cookie.indexOf("notificationClicked=on") != -1) {
  showNotifications();
} else if (document.cookie.indexOf("notificationClicked=off") != -1) {
  hideNotifications();
}

var option = document.querySelectorAll(".filter_options");
for (var i = 0; i < option.length; i++) {
  option[i].addEventListener("click", function () {
    var id = this.classList[0];
    console.log(id);
    var cL = document.getElementById(id).classList;
    console.log(cL);
    if (cL.contains("expand-section")) {
      cL.remove("expand-section");
      cL.add("hide-section");
    } else {
      cL.remove("hide-section");
      cL.add("expand-section");
    }
  });
}
function closeApplicantList() {
  document.getElementById("applicantList").style.display = "none";
}
function myFunction() {
  var element = document.getElementById("show");
  element.classList.add("popuppostshown");
  element.classList.remove("popupposthidden");
  element.style.display = "block";
  var element2 = document.getElementById("overlay");
  element2.classList.remove("hidden");
  element2.classList.add("show1");
  element2.style.display = "block";
}

// var projectInfo = document.querySelector('#projectInfo')
// var projects = document.querySelectorAll('.project')
// let info = projects[0].querySelectorAll('h1');
// for (let i = 0; i < projects.length; i++){
//   projects[i].addEventListener('click', function (){
//     let info = projects[i].querySelectorAll('h1');
//     let popupinfo = projectInfo.querySelectorAll('h1');
//     console.log(info[i]);
//     })
// }
console.log(1);
function notBubbleUp(e) {
  e.stopImmediatePropagation();
}

function closeProjInfo() {
  let x = document.getElementById("projectInfo");
  x.style.display = "none";
  var element = document.getElementById("projectInfo");
  element.classList.add("popupposthidden");
  element.classList.remove("popuppostshown");
  var element2 = document.getElementById("overlay2");
  element2.classList.add("hidden");
  element2.classList.remove("show1");
}


