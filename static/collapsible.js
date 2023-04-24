let toggleButtons = document.querySelectorAll('[data-table-id]');

for (let i = 0; i < toggleButtons.length; i++) {
    toggleButtons[i].addEventListener('click', function() {
        let tableId = toggleButtons[i].getAttribute('data-table-id');
        let table = document.getElementById(tableId + '-table');
        if (table.style.display === 'none') {
            table.style.display = 'table';
        } else {
            table.style.display = 'none';
        }
    });
}

// Get all the tables


// Add a click event listener to the "Collapse All" button
document.getElementById('btn-collapse-all').addEventListener('click', function () {
	// Loop through all the tables and set their display property to "none"
	for (let i = 0; i < toggleButtons.length; i++) {
        let tableId = toggleButtons[i].getAttribute('data-table-id');
        let table = document.getElementById(tableId + '-table');
		table.style.display = 'none';
	}
});
