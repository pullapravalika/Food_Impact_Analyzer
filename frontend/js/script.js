// Login form handler
document.addEventListener("DOMContentLoaded", function(){

    const loginForm = document.querySelector("form");

    if(loginForm){

        loginForm.addEventListener("submit", function(event){

            event.preventDefault();

            alert("Login functionality will connect to backend soon!");

        });

    }

});


// Register form handler
function registerUser(){

    alert("User registration will be connected to backend!");

}


// Food analysis handler
function analyzeFood(){

    alert("Food will be analyzed once backend API is ready!");

}