// LOGIN

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

alert(data.message)

if(data.message === "Login successful"){

localStorage.setItem("loggedIn","true")

window.location.href="/food_input_page"

}

})
// REGISTER

document.getElementById("registerForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const name = document.getElementById("name").value
const email = document.getElementById("email").value
const password = document.getElementById("password").value

try{

const response = await fetch("/register",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
name:name,
email:email,
password:password
})

})

const data = await response.json()

alert(data.message)

if(data.message === "User registered successfully"){
window.location.href="/login_page"
}

}catch(error){

alert("Registration failed")

}

})
// -------- FOOD ANALYSIS --------

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

.then(res=>res.json())
.then(data=>{

localStorage.setItem("foodResult",JSON.stringify(data))

window.location.href="/dashboard_page"

})

}


// -------- DASHBOARD --------

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
function updateStreak(category){

let healthy = parseInt(localStorage.getItem("healthyStreak")) || 0
let junk = parseInt(localStorage.getItem("junkStreak")) || 0

if(category === "healthy"){

healthy++
junk = 0

}else{

junk++
healthy = 0

}

localStorage.setItem("healthyStreak",healthy)
localStorage.setItem("junkStreak",junk)

}
if(document.getElementById("healthyStreak")){

document.getElementById("healthyStreak").textContent =
localStorage.getItem("healthyStreak") || 0

document.getElementById("junkStreak").textContent =
localStorage.getItem("junkStreak") || 0

}
if(document.getElementById("healthyStreak")){

document.getElementById("healthyStreak").textContent =
localStorage.getItem("healthyStreak") || 0

document.getElementById("junkStreak").textContent =
localStorage.getItem("junkStreak") || 0

}