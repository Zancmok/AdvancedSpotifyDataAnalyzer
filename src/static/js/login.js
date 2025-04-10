function passwordCompare(){
    var signupPassword = document.getElementById("signup-password").value
    var confirmPassword = document.getElementById("confirm-password").value
    if(signupPassword != confirmPassword){
        alert("get rect")
    }
}