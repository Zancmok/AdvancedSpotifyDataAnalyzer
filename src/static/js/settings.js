const newPassword = document.getElementById("new-password")
const confirmNewPassword = document.getElementById("confirm-new-password")
const matchPass = document.getElementById("passwordMatch");
const ChangeData = document.getElementById("user-data");
	
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

function uploadZip() {
	const fileInput = document.getElementById('zipFile');
	const formData = new FormData();

	if (fileInput.files.length === 0) {
		alert("Please select a ZIP file.");
		return;
	}

	formData.append("file", fileInput.files[0]);

	fetch(zipUploadUrl, {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			alert('File uploaded successfully!');
		} else {
			alert(data.reason);
		}
	})
	.catch(error => {
		console.error('Error:', error);
		alert('An error occurred while uploading the file.');
	});
}

function userDataChange(event){
	event.preventDefault();
	var passwordChanged = true
	if (newPassword.value === "" && confirmNewPassword.value === "") {
		passwordChanged = false;
	} else if (newPassword.value !== confirmNewPassword.value) {
		passwordChanged = false
	}
	const pfpChanged = fileInput.files.length > 0;
	const formData = new FormData();

	if (pfpChanged) {
        formData.append("pfp", fileInput.files[0]);
    }
	else
	{
		formData.append("pfp",null);
	}

	var usernameChanged = document.getElementById("new-username").value.lenght > 0;

	formData.append("old_password", document.getElementById("current-password").value);
	formData.append("new_username", document.getElementById("new-username").value)
	formData.append("username_changed", usernameChanged);
    formData.append("new_password", newPassword.value);
    formData.append("password_changed", passwordChanged);
    formData.append("pfp_changed", pfpChanged);

	fetch(settingUrl, {
        method: "POST",
        body: JSON.stringify(Object.fromEntries(formData))
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("User data updated successfully!");
        } else {
            alert(data.reason);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while updating the user data.");
    });

}
ChangeData.addEventListener("submit", userDataChange)
