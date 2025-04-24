function logoutPress(event){
	event.preventDefault();

	const logout_data = {
		type: "LOGOUT"
	};

	fetch(logoutUrl, { // Made this IP somehow dynamic
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(logout_data)
	})
	.then(res => {
		if (!res.ok) throw new Error(`Server error ${res.status}`);
		return res.json();
	})
	.then(data => {
		console.log("Server response:", data);
		if (data.success){
			window.location.assign(loginUrl);
		} 
		
	})
	.catch(err => {
		console.error("Fetch error:", err);
	});
}
login.addEventListener("submit", logoutPress)