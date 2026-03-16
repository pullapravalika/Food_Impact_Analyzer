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



const restaurantMenus = {

pizza_hut:[
{
food:"pizza",
price:250,
category:"junk",
image:"https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"
},

{
food:"veg pizza",
price:220,
category:"junk",
image:"https://images.unsplash.com/photo-1601924638867-3ec2f90b7c15"
}
],

burger_king:[
{
food:"burger",
price:180,
category:"junk",
image:"https://images.unsplash.com/photo-1550547660-d9450f859349"
},

{
food:"cheese burger",
price:200,
category:"junk",
image:"https://images.unsplash.com/photo-1550317138-10000687a72b"
}
],

green_bowl:[
{
food:"salad",
price:150,
category:"healthy",
image:"https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
},

{
food:"protein bowl",
price:180,
category:"healthy",
image:"https://images.unsplash.com/photo-1512621776951-a57141f2eefd"
}
],

south_india:[
{
food:"idli",
price:60,
category:"healthy",
image:"https://images.unsplash.com/photo-1589308078059-be1415eab4c3"
},

{
food:"dosa",
price:80,
category:"healthy",
image:"https://images.unsplash.com/photo-1631515242808-497c3fbd3972"
}
]

}



// ================= OPEN RESTAURANT =================

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

<img src="${item.image}" class="food-img">

<h3>${item.food}</h3>

<p class="price">₹${item.price}</p>

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

list.innerHTML = ""

cart.forEach((item,index)=>{

let li = document.createElement("li")

li.innerHTML = `
${item.food} - ₹${item.price}
<button onclick="removeItem(${index})">❌</button>
`

list.appendChild(li)

total += item.price

})

document.getElementById("cartTotal").textContent = total

}



// ================= REMOVE CART ITEM =================

function removeItem(index){

let cart = JSON.parse(localStorage.getItem("cart")) || []

cart.splice(index,1)

localStorage.setItem("cart",JSON.stringify(cart))

location.reload()

}



// ================= PLACE ORDER =================

function placeOrder(){

let cart = JSON.parse(localStorage.getItem("cart")) || []

if(cart.length === 0){

alert("Your cart is empty!")

return

}

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

alert("Order placed successfully!")

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



// TOTAL CALORIES

if(document.getElementById("calorieTotal")){
document.getElementById("calorieTotal").textContent = totalCalories
}



// WATER INTAKE

if(document.getElementById("waterSuggestion")){

let glasses = Math.ceil(totalCalories / 300)

document.getElementById("waterSuggestion").textContent =
"Drink about " + glasses + " glasses of water today."

}



// STREAKS

if(document.getElementById("healthyStreak")){
document.getElementById("healthyStreak").textContent =
localStorage.getItem("healthyStreak") || 0
}

if(document.getElementById("junkStreak")){
document.getElementById("junkStreak").textContent =
localStorage.getItem("junkStreak") || 0
}



// WEEKLY REPORT

if(document.getElementById("healthyDays")){
document.getElementById("healthyDays").textContent = healthyCount
}

if(document.getElementById("junkDays")){
document.getElementById("junkDays").textContent = junkCount
}



// ORDER HISTORY

if(document.getElementById("orderHistory")){

const list = document.getElementById("orderHistory")

orders.forEach(food=>{

let li = document.createElement("li")

li.textContent = food

list.appendChild(li)

})

}

}

}

// ================= FOOD SEARCH =================

function searchFood(){

let input = document.getElementById("foodSearch").value.toLowerCase()

let cards = document.querySelectorAll(".restaurant-card")

cards.forEach(card => {

let foodName = card.querySelector("h3").textContent.toLowerCase()

if(foodName.includes(input)){

card.style.display = "block"

}else{

card.style.display = "none"

}

})

}