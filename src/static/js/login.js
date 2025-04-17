const signupPassword = document.getElementById("signup-password")
const confirmPassword = document.getElementById("confirm-password")
const matchPass = document.getElementById("matchPass");
	
function comparePasswords() {
	if (signupPassword.value === "" && confirmPassword.value === "") {
		matchPass.textContent = "";
	} else if (signupPassword.value === confirmPassword.value) {
		matchPass.textContent = "✅ Passwords match!";
		matchPass.style.color = "green";
	} else {
		matchPass.textContent = "❌ Passwords do not match.";
		matchPass.style.color = "red";
	}
}

signupPassword.addEventListener("input", comparePasswords);
confirmPassword.addEventListener("input", comparePasswords);

const signup_data = {
	type: "SIGNUP",
	name: document.getElementById("signup-name").value,
	password: signupPassword
};

const login_data = {
	type: "LOGIN",
	name: document.getElementById("login-name").value,
	password: document.getElementById("login-password").value
};

function signupPress(){
	if (signupPassword.value === "" && confirmPassword.value === "") {
		return;
	} else if (signupPassword.value !== confirmPassword.value) {
		return;
	}

	let signup_data = {
		type: "SIGNUP",
		name: document.getElementById("signup-name").value,
		password: signupPassword
	};

	fetch('http://localhost:5000/login', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(signup_data)
	})
}