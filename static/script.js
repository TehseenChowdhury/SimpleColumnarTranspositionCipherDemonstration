async function sendData(endpoint) {
    // 1. GET DATA FROM HTML INPUTS
    const key = document.getElementById('keyInput').value;
    const msg = document.getElementById('messageInput').value;

    if (!key || !msg) {
        alert("Please enter both a Key and a Message.");
        return;
    }

    // 2. SEND DATA TO PYTHON (Using Fetch API)
    // We send a POST request to localhost:5000/encrypt (or /decrypt)
    const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ key: key, message: msg })
    });

    // 3. GET RESPONSE FROM PYTHON
    const data = await response.json();

    // 4. UPDATE THE UI
    document.getElementById('outputBox').innerText = data.result;
    
    // Call helper to draw the table
    drawGrid(data.grid, key);
}

function drawGrid(gridData, key) {
    const container = document.getElementById('gridContainer');
    container.innerHTML = ""; // Clear previous grid

    const table = document.createElement('table');

    // Create Header Row (The Key)
    const headerRow = document.createElement('tr');
    // We assume the grid width matches key length
    for (let char of key.toUpperCase()) {
        const cell = document.createElement('td');
        cell.innerText = char;
        cell.style.backgroundColor = "#2c3e50"; // Dark header
        cell.style.color = "white";
        headerRow.appendChild(cell);
    }
    // Wrap header in THEAD for proper HTML structure
    const thead = document.createElement('thead');
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create Data Rows (The Grid)
    const tbody = document.createElement('tbody');
    for (let row of gridData) {
        const tr = document.createElement('tr');
        for (let cellData of row) {
            const td = document.createElement('td');
            td.innerText = cellData;
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    container.appendChild(table);
}