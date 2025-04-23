const signupPassword = document.getElementById("signup-password")
const confirmPassword = document.getElementById("confirm-password")
const matchPass = document.getElementById("matchPass");
const form = document.getElementById("kurwaForm")

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

function signupPress(event){
	event.preventDefault();
	
	if (signupPassword.value === "" && confirmPassword.value === "") {
		return;
	} else if (signupPassword.value !== confirmPassword.value) {
		return;
	}

	let signup_data = {
		type: "SIGNUP",
		name: document.getElementById("signup-name").value,
		password: signupPassword.value
	};

	fetch('http://127.0.0.1:5000/login', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(signup_data)
	})
	.then(res => {
		if (!res.ok) throw new Error(`Server error ${res.status}`);
		return res.json();
	})
	.then(data => {
		console.log("Server response:", data);
		if (data.success) {
			matchPass.textContent = "✅ Account succesfully created";
			matchPass.style.color = "green";
		}
		else {
			matchPass.textContent = `❌ ${data.reason}`;
			matchPass.style.color = "red";
		}
	})
	.catch(err => {
		console.error("Fetch error:", err);
	});
}

form.addEventListener("submit", signupPress)


function loginPress(event){
	event.preventDefault();

	const login_data = {
		type: "LOGIN",
		name: document.getElementById("login-name").value,
		password: document.getElementById("login-password").value
	};

	fetch('http://127.0.0.1:5000/login', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(login_data)
	})
	.then(res => {
		if (!res.ok) throw new Error(`Server error ${res.status}`);
		return res.json();
	})
	.then(data => {
		// bim bim bam password stuff
		console.log("Server response:", data);
	})
	.catch(err => {
		console.error("Fetch error:", err);
	});
}