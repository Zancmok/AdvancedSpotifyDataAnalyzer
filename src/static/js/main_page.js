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

function getDateRangeFromSelection(selection) {
    const today = new Date();
    let startDate, endDate;

    endDate = new Date(today); // default to today

    switch (selection) {
        case "last-month":
            startDate = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
            break;
        case "last-year":
            startDate = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());
            break;
        case "all-time":
        default:
            startDate = new Date(1970, 0, 1); // UNIX epoch or a placeholder "start of time"
            break;
    }

    return {
        start: startDate.toISOString().split('T')[0], // Format: YYYY-MM-DD
        end: endDate.toISOString().split('T')[0]
    };
}


function getSelectedDateRange() {
    const dateRangeSelect = document.getElementById("date-range");
    return dateRangeSelect.value;
}

function getActualDateRange() {
    const selection = getSelectedDateRange();
    return getDateRangeFromSelection(selection);
}

function updateData() {
    const dateRange = getActualDateRange();

    const data = {
        start_date: dateRange.start,
        end_date: dateRange.end
    };

    fetch(dataUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(res => {
        if (!res.ok) throw new Error(`Server error ${res.status}`);
        return res.json();
    })
    .then(data => {
        console.log("Server response:", data);
        // do something with response
    })
    .catch(err => {
        console.error("Fetch error:", err);
    });
}

function refreshContent() {
    // Clear all lists
    document.getElementById("usersList").innerHTML = '';
    document.getElementById("genresList").innerHTML = '';
    document.getElementById("creatorsList").innerHTML = '';
    document.getElementById("albumsList").innerHTML = '';

    // Reset counters
    counters.users = 0;
    counters.genres = 0;
    counters.creators = 0;
    counters.albums = 0;

    // Optionally, reload default items (you can customize this part as needed)
    addTopUser();
    addTopGenre();
    addTopCreator();
    addTopAlbum();

    // Reload the data based on the selected date range
    updateData();
}