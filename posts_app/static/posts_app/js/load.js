

function navbarDrop(){
    // if(document.getElementById('navbar-toggler').getAttribute('aria-expanded')=='true'){
    // document.getElementById('navbar-toggler').setAttribute("aria-expanded","false");
    // document.getElementById('navbar-toggler').classList.add("collapsed");
    // }
    // else if(document.getElementById('navbar-toggler').getAttribute('aria-expanded')=='false'){
    //     document.getElementById('navbar-toggler').setAttribute('aria-expanded','true');
    //     document.getElementById('navbar-toggler').classList.remove("collapsed");
    // }
        // document.getElementById("navbar-toggler").setAttribute("aria-expanded","false");
    if(document.getElementById("navbarSupportedContent").className=="navbar-collapse collapse show"||document.getElementById("navbarSupportedContent").className=="navbar-collapse collapsing"){
        document.getElementById("navbarSupportedContent").className="collapse navbar-collapse";
        var x =document.querySelectorAll(".nav-link");
       for(var i =0;i<x.length;i++){
           x[i].style.marginBottom="0px";
       }
    }
    else{
        console.log("bye");
       document.getElementById("navbarSupportedContent").className="navbar-collapse collapse show";
       var x =document.querySelectorAll(".nav-link");
       for(var i =0;i<x.length;i++){
           x[i].style.marginBottom="10px";
       }
    }
}

function showNotifications() {
    document.cookie="notificationClicked=on";
   
    var box = document.getElementById("notification-box");
    k
    // 
    // box.classList.add("show2");
    // }
    // else{
    //     box.classList.remove("show2");
    //     box.classList.add("hide1");
    // }
    if(box.classList.contains("hide1")){
        box.classList.remove("hide1");
    }
        box.classList.add("show2");
}
function hideNotifications(){
    var box = document.getElementById("notification-box");
    document.cookie="notificationClicked=off";
   
    if(box.classList.contains("show2")){
        box.classList.remove("show2");
    }
        box.classList.add("hide1");
}
    
