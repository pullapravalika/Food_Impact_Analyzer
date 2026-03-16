// ================= LOGIN =================

document.getElementById("loginForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const email = document.getElementById("loginEmail").value
const password = document.getElementById("loginPassword").value

try{

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

window.location.href="/restaurants.html"

}

}catch(error){

alert("Login failed")

}

})


// ================= REGISTER =================

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

window.location.href="/login.html"

}

}catch(error){

alert("Registration failed")

}

})


// ================= RESTAURANT MENUS =================

const restaurantMenus = {

pizza_hut: [
{food:"pizza",price:250,category:"junk"},
{food:"veg pizza",price:220,category:"junk"}
],

burger_king: [
{food:"burger",price:180,category:"junk"},
{food:"cheese burger",price:200,category:"junk"}
],

green_bowl: [
{food:"salad",price:150,category:"healthy"},
{food:"protein bowl",price:180,category:"healthy"}
],

south_india: [
{food:"idli",price:60,category:"healthy"},
{food:"dosa",price:80,category:"healthy"}
]

}


// ================= OPEN MENU =================

function openMenu(name){

localStorage.setItem("restaurant",name)

window.location.href="/menu.html"

}


// ================= LOAD MENU =================

if(document.getElementById("menuItems")){

const restaurant = localStorage.getItem("restaurant")

const menu = restaurantMenus[restaurant]

const container = document.getElementById("menuItems")

document.getElementById("restaurantName").textContent =
restaurant.replace("_"," ").toUpperCase()

menu.forEach(item=>{

const card = document.createElement("div")

card.className="restaurant-card"

card.innerHTML = `

<h3>${item.food}</h3>
<p>₹${item.price}</p>

<button onclick="addToCart('${item.food}',${item.price},'${item.category}')">
Add to Cart
</button>

`

container.appendChild(card)

})

}


// ================= ADD TO CART =================

function addToCart(food,price,category){

let cart = JSON.parse(localStorage.getItem("cart")) || []

cart.push({
food:food,
price:price,
category:category
})

localStorage.setItem("cart",JSON.stringify(cart))

alert("Added to cart")

}


// ================= SHOW CART =================

if(document.getElementById("cartItems")){

let cart = JSON.parse(localStorage.getItem("cart")) || []

let list = document.getElementById("cartItems")

let total = 0

cart.forEach(item=>{

let li = document.createElement("li")

li.textContent = item.food + " - ₹" + item.price

list.appendChild(li)

total += item.price

})

document.getElementById("cartTotal").textContent = total

}


// ================= PLACE ORDER =================

function placeOrder(){

let cart = JSON.parse(localStorage.getItem("cart")) || []

let orders = JSON.parse(localStorage.getItem("orders")) || []

cart.forEach(item=>{

fetch("/place_order",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
user_id:1,
food_name:item.food,
price:item.price,
category:item.category
})

})

orders.push(item.food)

})

localStorage.setItem("orders",JSON.stringify(orders))

localStorage.removeItem("cart")

alert("Order placed successfully")

window.location.href="/dashboard.html"

}


// ================= DASHBOARD =================

window.onload=function(){

if(window.location.pathname.includes("dashboard")){

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

if(document.getElementById("calorieTotal")){
document.getElementById("calorieTotal").textContent = totalCalories
}

if(document.getElementById("waterSuggestion")){

let glasses = Math.ceil(totalCalories / 300)

document.getElementById("waterSuggestion").textContent =
"Drink about " + glasses + " glasses of water today."

}

}

}