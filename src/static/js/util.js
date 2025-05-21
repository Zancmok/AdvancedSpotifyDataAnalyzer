function createUser(userId, username, playtimeMs)
{
    const avatarUrl = `${baseUrl}/avatar/${userId}`
    const playtimeHrs = `${(playtimeMs / 3600000).toFixed(0)}hrs ${((playtimeMs % 3600000) / 60000).toFixed(0)}min`;

    const listItem = document.createElement("li");
    listItem.className = "list-group-item fade-in";
    listItem.innerHTML = `
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="${avatarUrl}" alt="${username}'s Avatar" style="width: 50px; height: 50px;">
            <span style="width: 100px;"><a href="${baseUrl}/user/${userId}">${username}</a></span>
            <span style="width: 80px;">${playtimeHrs}</span>
        </div>
    `;

    return listItem
}

function createTrack(trackId, track, trackUri, trackPFP, playtimeMs)
{
    const playtimeHrs = `${(playtimeMs / 3600000).toFixed(0)}hrs ${((playtimeMs % 3600000) / 60000).toFixed(0)}min`;

    const listItem = document.createElement("li");
    listItem.className = "list-group-item fade-in";
    listItem.innerHTML = `
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="${trackPFP}" alt="${track}'s Avatar" style="width: 50px; height: 50px;">
            <span style="width: 100px;"><a href="${baseUrl}/song/${trackId}">${track}</a></span>
            <span style="width: 80px;">${playtimeHrs}</span>
        </div>
    `;

    return listItem
}

function createGenre(genreId, genre, playtimeMs)
{
    const playtimeHrs = `${(playtimeMs / 3600000).toFixed(0)}hrs ${((playtimeMs % 3600000) / 60000).toFixed(0)}min`;

    const listItem = document.createElement("li");
    listItem.className = "list-group-item fade-in";
    listItem.innerHTML = `
        <div style="display: flex; align-items: center; gap: 20px;">
            <span style="width: 100px;"><a href="${baseUrl}/genre/${genreId}">${genre}</a></span>
            <span style="width: 80px;">${playtimeHrs} hrs</span>
        </div>
    `;

    return listItem
}

function createAuthor(authorId, author, authorUri, authorPFP, playtimeMs)
{
    const playtimeHrs = `${(playtimeMs / 3600000).toFixed(0)}hrs ${((playtimeMs % 3600000) / 60000).toFixed(0)}min`;

    const listItem = document.createElement("li");
    listItem.className = "list-group-item fade-in";
    listItem.innerHTML = `
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="${authorPFP}" alt="${author}'s Avatar" style="width: 50px; height: 50px;">
            <span style="width: 100px;"><a href="${baseUrl}/author/${authorId}">${author}</a></span>
            <span style="width: 80px;">${playtimeHrs} hrs</span>
        </div>
    `;

    return listItem
}

function createAlbum(albumId, album, albumUri, albumPFP, author, playtimeMs)
{
    const playtimeHrs = `${(playtimeMs / 3600000).toFixed(0)}hrs ${((playtimeMs % 3600000) / 60000).toFixed(0)}min`;

    const listItem = document.createElement("li");
    listItem.className = "list-group-item fade-in";
    listItem.innerHTML = `
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="${albumPFP}" alt="${album}'s Avatar" style="width: 50px; height: 50px;">
            <span style="width: 100px;"><a href="${baseUrl}/album/${albumId}">${album}</a></span>
            <span style="width: 80px;">${playtimeHrs} hrs</span>
        </div>
    `;

    return listItem
}
