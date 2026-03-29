// =======================
// REGISTER
// =======================

document.getElementById("registerForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const name = document.getElementById("name").value
const email = document.getElementById("email").value
const password = document.getElementById("password").value

try{

const res = await fetch("/register",{
method:"POST",
headers:{ "Content-Type":"application/json" },
body:JSON.stringify({ name,email,password })
})

const data = await res.json()
alert(data.message)

if(data.message === "User registered successfully"){
window.location.href = "/login_page"
}

}catch(error){
alert("Registration failed")
}

})


// =======================
// LOGIN
// =======================

document.getElementById("loginForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const email = document.getElementById("loginEmail").value
const password = document.getElementById("loginPassword").value

try{

const response = await fetch("/login",{
method:"POST",
headers:{ "Content-Type":"application/json" },
body:JSON.stringify({ email,password })
})

const data = await response.json()

if(data.message === "Login successful"){

alert("Login Successful")

localStorage.setItem("userId", data.user_id)

// ✅ UPDATED FLOW
window.location.href = "/restaurants_page"

}else{
alert(data.message)
}

}catch(error){
alert("Login failed")
}

})


// =======================
// RESTAURANT → MENU FLOW
// =======================

function openMenu(restaurant){
localStorage.setItem("restaurant", restaurant)
window.location.href = "/menu_page"
}


// =======================
// MENU LOAD
// =======================

if(window.location.pathname.includes("menu_page")){

const restaurant = localStorage.getItem("restaurant")

document.getElementById("restaurantName").innerText = restaurant.toUpperCase()

const menu = {

dominos:[
{name:"Pizza", price:200, img:"https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"},
{name:"Garlic Bread", price:120, img:"https://images.unsplash.com/photo-1603079841964-6d2e1c6c3c57"}
],

kfc:[
{name:"Chicken Burger", price:150, img:"https://images.unsplash.com/photo-1550547660-d9450f859349"},
{name:"Fried Chicken", price:180, img:"https://images.unsplash.com/photo-1606755962773-d324e2c8c4b1"}
],

subway:[
{name:"Veg Sandwich", price:130, img:"https://images.unsplash.com/photo-1606755962773-d324e2c8c4b1"},
{name:"Salad", price:120, img:"https://images.unsplash.com/photo-1546069901-ba9599a7e63c"}
],

udupi:[
{name:"Idli", price:80, img:"https://images.unsplash.com/photo-1589308078059-be1415eab4c3"},
{name:"Dosa", price:100, img:"https://images.unsplash.com/photo-1604908554007-7a0b4d46b80e"}
]

}

const container = document.getElementById("menuItems")

container.innerHTML = ""

menu[restaurant].forEach(item=>{

const div = document.createElement("div")
div.className = "restaurant-card"

div.innerHTML = `
<img src="${item.img}">
<h3>${item.name}</h3>
<p>₹${item.price}</p>
<button onclick="addToCart('${item.name}',${item.price})">Add to Cart</button>
`

container.appendChild(div)

})

}


// =======================
// CART
// =======================

function addToCart(name, price){

let cart = JSON.parse(localStorage.getItem("cart")) || []

cart.push({name, price})

localStorage.setItem("cart", JSON.stringify(cart))

alert("Added to cart 🛒")

}


// =======================
// ORDER API (OPTIONAL)
// =======================

function orderFood(food, price){

const email = localStorage.getItem("userEmail")

fetch("/order_food",{
method:"POST",
headers:{ "Content-Type":"application/json" },
body:JSON.stringify({ food, price, email })
})
.then(res => res.json())
.then(()=>{

alert("Order placed successfully ✅")
window.location.href = "/dashboard_page"

})

}


// =======================
// DASHBOARD LOAD
// =======================

if(window.location.pathname.includes("dashboard_page")){

const email = localStorage.getItem("userEmail")

fetch("/dashboard_data/" + email)
.then(res => res.json())
.then(data => {

document.getElementById("calories").textContent = data.calories
document.getElementById("healthyCircle").textContent = data.healthy
document.getElementById("junkCircle").textContent = data.junk

// suggestions
if(data.junk > data.healthy){
document.getElementById("suggestions").innerText =
"⚠ Reduce junk food. Try healthy food like Salad 🥗"
}else{
document.getElementById("suggestions").innerText =
"✅ Good eating habits! Keep it up 💪"
}

drawChart(data.healthy, data.junk)
simulateDelivery()

})

}


// =======================
// CHART
// =======================

function drawChart(healthy, junk){

const ctx = document.getElementById("myChart")
if(!ctx) return

new Chart(ctx,{
type:'doughnut',
data:{
labels:['Healthy','Junk'],
datasets:[{ data:[healthy,junk] }]
}
})

}


// =======================
// DELIVERY
// =======================

function simulateDelivery(){

const status = document.getElementById("orderStatus")
if(!status) return

setTimeout(()=>status.innerText="Preparing...",1000)
setTimeout(()=>status.innerText="Out for Delivery 🚚",4000)
setTimeout(()=>status.innerText="Delivered ✅",8000)

}


// =======================
// RESET PASSWORD
// =======================

document.getElementById("resetForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const email = document.getElementById("resetEmail").value
const password = document.getElementById("newPassword").value

const res = await fetch("/reset_password",{
method:"POST",
headers:{ "Content-Type":"application/json" },
body:JSON.stringify({ email,password })
})

const data = await res.json()

alert(data.message)
window.location.href = "/login_page"

})


// =======================
// ACCOUNT PAGE
// =======================

if(window.location.pathname.includes("account_page")){

const email = localStorage.getItem("userEmail")

document.getElementById("userEmail").textContent = email

fetch("/get_orders/" + email)
.then(res => res.json())
.then(data => {

document.getElementById("totalOrders").textContent = data.length

const list = document.getElementById("orderList")
list.innerHTML = ""

data.forEach(order=>{

const div = document.createElement("div")
div.className = "menu-item"

div.innerHTML = `
<p><b>Food:</b> ${order[0]}</p>
<p><b>Price:</b> ₹${order[1]}</p>
<p><b>Category:</b> ${order[2]}</p>
<p><b>Time:</b> ${order[3]}</p>
<hr>
`

list.appendChild(div)

})

})

}


// =======================
// SUPPORT SYSTEM
// =======================

document.getElementById("supportForm")?.addEventListener("submit", async function(e){

e.preventDefault()

const email = localStorage.getItem("userEmail")
const issue = document.getElementById("issueType").value
const description = document.getElementById("description").value

const res = await fetch("/submit_issue",{
method:"POST",
headers:{ "Content-Type":"application/json" },
body:JSON.stringify({ email, issue, description })
})

const data = await res.json()
alert(data.message)

})


// =======================
// ADMIN PANEL
// =======================

if(window.location.pathname.includes("admin_page")){

fetch("/get_issues")
.then(res => res.json())
.then(data => {

const list = document.getElementById("issuesList")
list.innerHTML = ""

data.forEach(issue=>{

const div = document.createElement("div")
div.className = "menu-item"

div.innerHTML = `
<p><b>User:</b> ${issue[1]}</p>
<p><b>Issue:</b> ${issue[2]}</p>
<p><b>Description:</b> ${issue[3]}</p>
<p><b>Status:</b> ${issue[4]}</p>
<button onclick="resolveIssue(${issue[0]})">Resolve</button>
<hr>
`

list.appendChild(div)

})

})

}

function resolveIssue(id){
fetch("/resolve_issue/" + id,{ method:"POST" })
.then(()=>location.reload())
}

// =======================
// LOAD CART PAGE
// =======================

if(window.location.pathname.includes("cart_page")){

let cart = JSON.parse(localStorage.getItem("cart")) || []

const container = document.getElementById("cartItems")

let total = 0

container.innerHTML = ""

cart.forEach((item, index)=>{

total += item.price

const div = document.createElement("div")

div.className = "menu-item"

div.innerHTML = `
<p><b>${item.name}</b> - ₹${item.price}</p>
<button onclick="removeItem(${index})">Remove</button>
<hr>
`

container.appendChild(div)

})

document.getElementById("totalPrice").textContent = total

}


// REMOVE ITEM
function removeItem(index){

let cart = JSON.parse(localStorage.getItem("cart"))

cart.splice(index,1)

localStorage.setItem("cart", JSON.stringify(cart))

location.reload()

}


// GO TO PAYMENT
function goToPayment(){

window.location.href = "/payment_page"

}