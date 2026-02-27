function showMessage() {
    alert("Feature is working perfectly!");
}

function enableNewFeature() {
    document.getElementById("featureStatus").innerText =
        "New Feature Enabled Successfully!";
}

function loginUser() {

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (username === "" || password === "") {
        document.getElementById("loginMessage").innerText =
            "Please enter both fields.";
        return;
    }

    // INCOMPLETE AUTH LOGIC (Still Under Development)

    if (username === "admin" && password === "1234") {
        document.getElementById("loginMessage").innerText =
            "Login successful! (Role system not implemented yet)";
    } else {
        document.getElementById("loginMessage").innerText =
            "Invalid credentials (Database not connected yet)";
    }
}