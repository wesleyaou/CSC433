/* ==================
Login functions
================== */

function readEmailIn(){
    var emailAddress = document.getElementById("email-in").value;

    if (!validateEmail(emailAddress)) {
        return;
    }

    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var ajaxReturn = JSON.parse(this.responseText);
            window.emailAddress = emailAddress;
            if (ajaxReturn.email === true) {
                console.log("login");
                startLogin();
            } else if (ajaxReturn.email === false) {
                console.log("Reg");
                startRegistration();
            }
        }
    }

    req.open('POST', "/user/validate-email", true);
    req.setRequestHeader("Content-type", "application/json")
    req.send(JSON.stringify({"emailAddress" : emailAddress}));
}

function startRegistration() {
    var emailInput = document.getElementById("email-div");
    emailInput.style.display = "none";

    var passwordInput = document.getElementById("password-div");
    passwordInput.style.display = "grid";

    var passwordSubmit = document.getElementById("pass-submit")
    passwordSubmit.style.display = "none";

    var emailDisp = document.getElementById("email-display");
    emailDisp.innerHTML = window.emailAddress;

    var regDiv = document.getElementById("register-div");
    regDiv.style.display = "grid";

    var phoneNumIn = document.getElementById("phoneNumber-in");
    phoneNumIn.addEventListener("keypress", getPhoneCarrier);

}

function startLogin() {
    var emailInput = document.getElementById("email-div");
    emailInput.style.display = "none";

    var passwordInput = document.getElementById("password-div");
    passwordInput.style.display = "grid";

    var emailDisp = document.getElementById("email-display");
    emailDisp.innerHTML = window.emailAddress;

}

function submitLogin() {
    var password = document.getElementById("password-in").value;

    if (password === "" || emailAddress === " " || password.length < 6){
            alert("Invalid password!");
            return
    }

    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var ajaxReturn = JSON.parse(this.responseText);
            window.emailAddress = emailAddress;
            if (ajaxReturn.uid != null) {
                localStorage.setItem("_uid", ajaxReturn.uid);
                console.log("LOCAL: " + localStorage.getItem("_uid"))
                window.location = "/home";
                return;
            } else {
                alert(ajaxReturn.error);
            }
        }
    }

    req.open('POST', "/user/login", true);
    req.setRequestHeader("Content-type", "application/json")
    req.send(JSON.stringify({"emailAddress" : window.emailAddress, "password" : password}));
}

function submitReg() {
    var password = document.getElementById("password-in").value;
    var phoneNumber = document.getElementById("phoneNumber-in").value;
    var carrier = document.querySelector('input[name="cell-carrier"]:checked').value;
    var firstName = document.getElementById("firstname-in").value;
    var lastName = document.getElementById("lastname-in").value;
    var phoneNotifs = "false";
    var emailNotifs = "false";

    if (!(validatePassword(password))){
        return;
    }

    if (phoneNumber != ""){
        if (!(validatePhone(phoneNumber))) {
            return;
        } else {
            if (carrier === null || carrier === ""){
                alert("Please select a cell phone carrier!");
                return;
            } else {
                phoneNumber = phoneNumber + carrier;
            }
        }
    }

    notifPrefs = document.querySelectorAll('input[name="notif-prefs"]:checked');
    for (i=0;i < notifPrefs.length; i++){
        if (notifPrefs[i].value === "phoneNotifs") {
            phoneNotifs = "true";
        } else if (notifPrefs[i].value === "emailNotifs") {
            emailNotifs = "true";
        }
    }

    newUser = new Object();

    newUser.firstName = firstName;
    newUser.lastName = lastName;
    newUser.emailAddress = emailAddress;
    newUser.phoneNumber = phoneNumber;
    newUser.password = password;
    newUser.emailNotifs = emailNotifs;
    newUser.phoneNotifs = phoneNotifs;

    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var ajaxReturn = JSON.parse(this.responseText);
            window.emailAddress = emailAddress;
            if (ajaxReturn.success != null) {
                alert(ajaxReturn.success);
                location.reload();
                return;
            } else {
                alert(ajaxReturn.error);
            }
        }
    }

    req.open('POST', "/create/user", true);
    req.setRequestHeader("Content-type", "application/json")
    req.send(JSON.stringify(newUser));
}

function getPhoneCarrier() {
    var phoneNum = document.getElementById("phoneNumber-in").value;
    var carrierSelect = document.getElementById("pick-carrier");
    var phoneOpt = document.getElementById("phone-notifs-label");
    if (phoneNum != "" || phoneNum != null){
        carrierSelect.style.display = "grid";
        phoneOpt.style.display = "inline-block";
    }
}

/* ==================
Validation functions
================== */

function validateEmail(emailAddress) {
    if (emailAddress === "" || emailAddress === " " || 
    (!(emailAddress.includes("@"))) || (!(emailAddress.includes(".")))){
        alert("Please enter a valid email address!");
        return false;
    }

    return true;
}

function validatePassword(password) {
    if (password === "" || 
        password === " " ||
        password.length < 6) {
    alert("Password entered does not meet required criteria!")
    return false;
    }

    return true;
}

function validatePhone(phoneNumber) {
    var alphaRegExp = /[a-zA-Z]/g;
    console.log(phoneNumber.length)
    if ((alphaRegExp.test(phoneNumber) || phoneNumber.length < 10)) {
        alert("Invalid phone number entered!")
        return false;
    }
    
    return true;
}
