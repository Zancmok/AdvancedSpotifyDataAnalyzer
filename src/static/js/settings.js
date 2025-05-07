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
			alert('Error uploading file.');
		}
	})
	.catch(error => {
		console.error('Error:', error);
		alert('An error occurred while uploading the file.');
	});
}
