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
//Welcome Message
document.getElementById("userName").textContent =
localStorage.getItem("userName") || "User"
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

// UPDATE STREAK HERE
updateStreak(data.category)

window.location.href="/dashboard_page"

})

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
//Water Intake
let glasses = Math.ceil(totalCalories / 300)

document.getElementById("waterSuggestion").textContent =
"Drink about " + glasses + " glasses today"

let percent = Math.min((glasses / 8) * 100,100)

document.getElementById("waterProgress").style.width =
percent + "%"

document.getElementById("healthyBar").style.width =
(healthyCount * 20) + "%"

document.getElementById("junkBar").style.width =
(junkCount * 20) + "%"
// SHOW STREAKS

document.getElementById("healthyStreak").textContent =
localStorage.getItem("healthyStreak") || 0

document.getElementById("junkStreak").textContent =
localStorage.getItem("junkStreak") || 0


// ORDER HISTORY ANALYSIS

const orders = JSON.parse(localStorage.getItem("orders")) || []

const foodData = {

pizza:{calories:285,type:"junk"},
burger:{calories:350,type:"junk"},
salad:{calories:120,type:"healthy"},
idli:{calories:70,type:"healthy"}

}

let totalCalories = 0
let junkCount = 0
let healthyCount = 0

orders.forEach(food=>{

let data = foodData[food]

if(data){

totalCalories += data.calories

if(data.type==="junk"){
junkCount++
}else{
healthyCount++
}

}

})


// TOTAL CALORIES

if(document.getElementById("calorieTotal")){
document.getElementById("calorieTotal").textContent = totalCalories
}


// WATER SUGGESTION

if(document.getElementById("waterSuggestion")){

let glasses = Math.ceil(totalCalories / 300)

document.getElementById("waterSuggestion").textContent =
"Drink about " + glasses + " glasses of water today."

}


// WEEKLY REPORT

if(document.getElementById("healthyDays")){
document.getElementById("healthyDays").textContent = healthyCount
}

if(document.getElementById("junkDays")){
document.getElementById("junkDays").textContent = junkCount
}

}

}