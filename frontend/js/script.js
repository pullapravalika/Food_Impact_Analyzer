// ---------------------
// LOGIN
// ---------------------

document.getElementById("loginForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const email = document.getElementById("loginEmail").value
const password = document.getElementById("loginPassword").value

const response = await fetch("/login",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
email:email,
password:password
})
})

const data = await response.json()

if(data.message === "Login successful"){

window.location.href="/food_input_page"

}else{

alert(data.message)

}

})


// ---------------------
// FOOD ANALYSIS
// ---------------------

function analyzeFood(food){

fetch("/analyze_food",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
food:food
})

})

.then(res => res.json())
.then(data => {

localStorage.setItem("foodResult",JSON.stringify(data))

window.location.href="/dashboard_page"

})

}


// ---------------------
// DASHBOARD DISPLAY
// ---------------------

window.onload=function(){

if(window.location.pathname.includes("dashboard_page")){

const result=JSON.parse(localStorage.getItem("foodResult"))

if(result){

document.getElementById("foodItem").textContent=result.food
document.getElementById("calories").textContent=result.calories
document.getElementById("category").textContent=result.category
document.getElementById("healthScore").textContent=result.health_score

}

}

}