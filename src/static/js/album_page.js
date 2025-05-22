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
        body: JSON.stringify({ start_date: start, end_date: end, album_id: albumId })
    })
    .then(res => {
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        return res.json();
    })
    .then(data => {
        console.log("Updated user data:", data);

        const albumData = document.getElementById("album-data");
        const albumDataPFP = document.getElementById("album-data-pfp");

        albumData.innerHTML = data["main"][0][0]
        albumDataPFP.src = data["main"][0][1]

        const usersList = document.getElementById("usersList");
        const trackList = document.getElementById("tracksList");

        // Clear existing content
        usersList.innerHTML = "";
        trackList.innerHTML = "";

        data.users.forEach(([userId, username, playtimeMs]) => {
            usersList.appendChild(createUser(userId, username, playtimeMs));
        })

        data.tracks.forEach(([trackId, track, trackUri, trackPFP, playtimeMs]) => {
            trackList.appendChild(createTrack(trackId, track, trackUri, trackPFP, playtimeMs));
        })
    })
    .catch(err => console.error("Fetch error:", err));
}

document.getElementById("date-range").addEventListener("change", refreshContent)

// Initial load
refreshContent();
