const newPassword = document.getElementById("new-password")
const confirmNewPassword = document.getElementById("confirm-new-password")
const matchPass = document.getElementById("passwordMatch");
	
function comparePasswords() {
	if (newPassword.value === "" && confirmNewPassword.value === "") {
		matchPass.textContent = "";
	} else if (newPassword.value === confirmNewPassword.value) {
		matchPass.textContent = "✅ New Passwords match!";
		matchPass.style.color = "green";
	} else {
		matchPass.textContent = "❌ New passwords do not match.";
		matchPass.style.color = "red";
	}
}

newPassword.addEventListener("input", comparePasswords);
confirmNewPassword.addEventListener("input", comparePasswords);