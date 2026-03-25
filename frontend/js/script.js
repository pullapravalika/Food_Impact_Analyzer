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


// ==========================
// LOGIN
// ==========================

document.getElementById("loginForm")?.addEventListener("submit", async function(e) {

    e.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        // ✅ SUCCESS
        if (data.message === "Login successful") {

            alert("Login Successful");

            // Save user info
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("user_name", data.name);

            // 🔥 REDIRECT TO RESTAURANTS PAGE
            window.location.href = "http://127.0.0.1:5000/restaurants_page";

        } else {
            alert(data.message);
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Login failed");
    }
});


// =======================
// FOOD ORDER / ANALYSIS
// =======================

function analyzeFood(food){

const email = localStorage.getItem("userEmail") || "guest"

fetch("/analyze_food",{
method:"POST",
headers:{ "Content-Type":"application/json" },
body:JSON.stringify({ food,email })
})
.then(res => res.json())
.then(data => {

localStorage.setItem("foodResult", JSON.stringify(data))

window.location.href = "/dashboard_page"

})

}


// =======================
// DASHBOARD LOAD
// =======================

window.onload = function(){

if(window.location.pathname.includes("dashboard_page")){

const result = JSON.parse(localStorage.getItem("foodResult"))

if(result){

// Show values
document.getElementById("calories").textContent = result.calories
document.getElementById("healthScore").textContent = result.health_score

// Update streak
updateStreak(result.category)

// Show UI
showDashboard()

}

}

}

// ==========================
// OPEN MENU FUNCTION
// ==========================

function openMenu(restaurantName) {

    // Save selected restaurant
    localStorage.setItem("restaurant", restaurantName);

    // Redirect to menu page
    window.location.href = "http://127.0.0.1:5000/menu_page";
}

// =======================
// STREAK LOGIC
// =======================

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

localStorage.setItem("healthyStreak", healthy)
localStorage.setItem("junkStreak", junk)

}


// =======================
// DASHBOARD DISPLAY
// =======================

function showDashboard(){

let healthy = parseInt(localStorage.getItem("healthyStreak")) || 0
let junk = parseInt(localStorage.getItem("junkStreak")) || 0

// Circles
document.getElementById("healthyCircle").textContent = healthy
document.getElementById("junkCircle").textContent = junk

// Water suggestion (based on healthy streak)
let water = healthy * 20
if(water > 100) water = 100

document.getElementById("waterFill").style.width = water + "%"

// Suggestions
if(junk > 0){
document.getElementById("suggestions").innerText =
"⚠ Reduce junk food. Try Salad 🥗 or Idli 🥘"
}else{
document.getElementById("suggestions").innerText =
"✅ Excellent healthy eating! Keep it up 💪"
}

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

data.forEach(order => {

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

data.forEach(issue => {

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

fetch("/resolve_issue/" + id,{
method:"POST"
})
.then(()=>location.reload())

}