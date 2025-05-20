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
        body: JSON.stringify({ start_date: start, end_date: end, user_id: userId })
    })
    .then(res => {
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        return res.json();
    })
    .then(data => {
        console.log("Updated user data:", data);

        const userData = document.getElementById("user-data");

        userData.innerHTML = userId

        const genresList = document.getElementById("genresList");
        const trackList = document.getElementById("trackList");
        const creatorsList = document.getElementById("creatorsList");
        const albumsList = document.getElementById("albumsList");

        // Clear existing content
        genresList.innerHTML = "";
        trackList.innerHTML = "";
        creatorsList.innerHTML = "";
        albumsList.innerHTML = "";

        data.genres.forEach(([genreId, genre, playtimeMs]) => {
            genresList.appendChild(createGenre(genreId, genre, playtimeMs));
        })

        data.tracks.forEach(([trackId, track, trackUri, trackPFP, playtimeMs]) => {
            trackList.appendChild(createTrack(trackId, track, trackUri, trackPFP, playtimeMs));
        })

        data.authors.forEach(([authorId, author, authorUri, authorPFP, playtimeMs]) => {
            creatorsList.appendChild(createAuthor(authorId, author, authorUri, authorPFP, playtimeMs));
        })

        data.albums.forEach(([albumId, album, albumUri, albumPFP, author, playtimeMs]) => {

            albumsList.appendChild(createAlbum(albumId, album, albumUri, albumPFP, author, playtimeMs));
        })
    })
    .catch(err => console.error("Fetch error:", err));
}

// Initial load
refreshContent();
