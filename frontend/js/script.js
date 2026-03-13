// REGISTER

document.getElementById("registerForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const name = document.getElementById("name").value
const email = document.getElementById("email").value
const password = document.getElementById("password").value

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

})





// LOGIN

document.getElementById("loginForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const email = document.getElementById("loginEmail").value
const password = document.getElementById("loginPassword").value

const response = await fetch("http://127.0.0.1:5000/login",{

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

window.location.href = "/food_input_page"

}

})






// FOOD ANALYSIS

document.getElementById("foodForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const food = document.getElementById("foodName").value

const response = await fetch("http://127.0.0.1:5000/analyze_food",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
food:food
})

})

const data = await response.json()

localStorage.setItem("foodResult", JSON.stringify(data))

window.location.href = "/dashboard_page"

})






// DASHBOARD RESULT DISPLAY

if(window.location.pathname.includes("dashboard.html")){

const result = JSON.parse(localStorage.getItem("foodResult"))

if(result){

document.getElementById("foodItem").textContent = result.food
document.getElementById("calories").textContent = result.calories
document.getElementById("healthScore").textContent = result.health_score
document.getElementById("category").textContent = result.category

}
}
// DASHBOARD RESULT DISPLAY

if(window.location.pathname.includes("dashboard_page")){

const result = JSON.parse(localStorage.getItem("foodResult"))

if(result){

document.getElementById("foodItem").textContent = result.food
document.getElementById("calories").textContent = result.calories
document.getElementById("healthScore").textContent = result.health_score
document.getElementById("category").textContent = result.category

}

}