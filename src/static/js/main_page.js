// Function to add an item to a list
function addItemToList(listId, itemText) {
    const list = document.getElementById(listId);
    const newItem = document.createElement("li");
    newItem.classList.add("list-group-item", "fade-in");
    newItem.textContent = itemText;
    list.appendChild(newItem);
    
    // Scroll to bottom of container to show new item
    const container = list.parentElement;
    container.scrollTop = container.scrollHeight;
}

// Sample data for demonstrations
const users = ["Emily Davis", "Robert Wilson", "Jessica Lee", "David Miller", "Amanda White"];
const genres = ["Electronic", "R&B", "Jazz", "Country", "Classical"];
const creators = ["Billie Eilish", "Kendrick Lamar", "Ariana Grande", "Ed Sheeran", "Doja Cat"];
const albums = ["Planet Her", "DAMN.", "Happier Than Ever", "Divide", "Positions"];

// Counter to track which item to add next
const counters = {
    users: 0,
    genres: 0,
    creators: 0,
    albums: 0
};

// Functions to add items to each list
function addTopUser() {
    if (counters.users < users.length) {
        addItemToList("usersList", users[counters.users]);
        counters.users++;
    } else {
        // Start over when we run out of sample data
        counters.users = 0;
        addItemToList("usersList", users[counters.users]);
        counters.users++;
    }
}

function addTopGenre() {
    if (counters.genres < genres.length) {
        addItemToList("genresList", genres[counters.genres]);
        counters.genres++;
    } else {
        counters.genres = 0;
        addItemToList("genresList", genres[counters.genres]);
        counters.genres++;
    }
}

function addTopCreator() {
    if (counters.creators < creators.length) {
        addItemToList("creatorsList", creators[counters.creators]);
        counters.creators++;
    } else {
        counters.creators = 0;
        addItemToList("creatorsList", creators[counters.creators]);
        counters.creators++;
    }
}

function addTopAlbum() {
    if (counters.albums < albums.length) {
        addItemToList("albumsList", albums[counters.albums]);
        counters.albums++;
    } else {
        counters.albums = 0;
        addItemToList("albumsList", albums[counters.albums]);
        counters.albums++;
    }
}