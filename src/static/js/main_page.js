function getSelectedDateRange() {
    const select = document.getElementById("date-range");
    return select ? select.value : "all-time";
}

function getDateRangeFromSelection(selection) {
    const today = new Date();
    let startDate;

    switch (selection) {
        case "last-month":
            startDate = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
            break;
        case "last-year":
            startDate = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());
            break;
        default:
            startDate = new Date(1970, 0, 1);
    }

    return {
        start: startDate.toISOString().split('T')[0],
        end: today.toISOString().split('T')[0]
    };
}

function getActualDateRange() {
    return getDateRangeFromSelection(getSelectedDateRange());
}

function refreshContent() {
    const { start, end } = getActualDateRange();

    fetch(dataUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start_date: start, end_date: end })
    })
    .then(res => {
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        return res.json();
    })
    .then(data => {
        console.log("Updated user data:", data);

        const usersList = document.getElementById("usersList");
        const genresList = document.getElementById("genresList");
        const trackList = document.getElementById("trackList");
        const creatorsList = document.getElementById("creatorsList");
        const albumsList = document.getElementById("albumsList");

        // Clear existing content
        usersList.innerHTML = "";
        genresList.innerHTML = "";
        trackList.innerHTML = "";
        creatorsList.innerHTML = "";
        albumsList.innerHTML = "";

        data.users.forEach(([userId, username, playtimeMs]) => {
            const avatarUrl = `avatar/${userId}`
            const playtimeHrs = (playtimeMs / 3600000).toFixed(0);

            const listItem = document.createElement("li");
            listItem.className = "list-group-item fade-in";
            listItem.innerHTML = `
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="${avatarUrl}" alt="${username}'s Avatar" style="width: 50px; height: 50px;">
                    <span style="width: 100px;">${username}</span>
                    <span style="width: 80px;">${playtimeHrs} hrs</span>
                </div>
            `;
            usersList.appendChild(listItem);
        });

        data.genres.forEach(([genreId, genre, playtimeMs]) => {
            const playtimeHrs = (playtimeMs / 3600000).toFixed(0);

            const listItem = document.createElement("li");
            listItem.className = "list-group-item fade-in";
            listItem.innerHTML = `
                <div style="display: flex; align-items: center; gap: 20px;">
                    <span style="width: 100px;">${genre}</span>
                    <span style="width: 80px;">${playtimeHrs} hrs</span>
                </div>
            `;
            genresList.appendChild(listItem);
        })

        data.tracks.forEach(([trackId, track, trackUri, trackPFP, playtimeMs]) => {
            const playtimeHrs = `${(playtimeMs / 3600000).toFixed(0)}hrs ${((playtimeMs % 3600000) / 60000).toFixed(0)}min`;

            const listItem = document.createElement("li");
            listItem.className = "list-group-item fade-in";
            listItem.innerHTML = `
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="${trackPFP}" alt="${track}'s Avatar" style="width: 50px; height: 50px;">
                    <span style="width: 100px;">${track}</span>
                    <span style="width: 80px;">${playtimeHrs}</span>
                </div>
            `;
            trackList.appendChild(listItem);
        })

        data.authors.forEach(([authorId, author, authorUri, authorPFP, playtimeMs]) => {
            const playtimeHrs = (playtimeMs / 3600000).toFixed(0);

            const listItem = document.createElement("li");
            listItem.className = "list-group-item fade-in";
            listItem.innerHTML = `
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="${authorPFP}" alt="${author}'s Avatar" style="width: 50px; height: 50px;">
                    <span style="width: 100px;">${author}</span>
                    <span style="width: 80px;">${playtimeHrs} hrs</span>
                </div>
            `;
            creatorsList.appendChild(listItem);
        })

        data.albums.forEach(([albumId, album, albumUri, albumPFP, author, playtimeMs]) => {
            const playtimeHrs = (playtimeMs / 3600000).toFixed(0);

            const listItem = document.createElement("li");
            listItem.className = "list-group-item fade-in";
            listItem.innerHTML = `
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="${albumPFP}" alt="${album}'s Avatar" style="width: 50px; height: 50px;">
                    <span style="width: 100px;">${album}</span>
                    <span style="width: 80px;">${playtimeHrs} hrs</span>
                </div>
            `;
            albumsList.appendChild(listItem);
        })
    })
    .catch(err => console.error("Fetch error:", err));
}

// Initial load
refreshContent();
