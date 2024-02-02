// Makes API call to delete swimmer event
function deleteSwimmerEvent(event, name) {
	fetch('/delete_swimmer', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			event : event,
			name : name
		})
	})
	.then(response => {
		if (response.ok) {
			// Handle successful response here
			console.log('Swimmer deleted successfully!');
		} else {
			// Handle error response here
			console.error('Error deleting swimmer:', response.statusText);
		}
	})
	.catch(error => {
		// Handle network error here
		console.error('Network error:', error);
	});
}

function updatePointTotals() {
  fetch('/points_by_team')
    .then(response => response.json())
    .then(data => {
		for (let key in data) {
			document.querySelector(`#team-points-${key.split(" ")[0]}`).innerHTML = `${key}: ${data[key]}`;
		}
      });
}

// add a click event listener to each delete button
let deleteButtons = document.querySelectorAll('.delete-button');
deleteButtons.forEach(button => {
  button.addEventListener('click', function() {
    // get the swimmer name and event name from the data attributes
    let swimmerName = this.getAttribute('data-swimmer-name');
    let eventName = this.getAttribute('data-swimmer-event');

    // delete the entry from the entries_by_team data
	deleteSwimmerEvent(eventName, swimmerName);

    // update the table
    let tableId = swimmerName + '-table';
	tableId = tableId.replace(' ', '');
	console.log('tableId: ' + tableId);
    let table = document.getElementById(tableId);
    let row = this.parentNode.parentNode;
	let eventPoints = row.querySelector('td:nth-child(5)').textContent;
    table.deleteRow(row.rowIndex);

	// Get a reference to the element with id = swimmer_name
	let swimmerDiv = document.getElementById(swimmerName.replace(' ', '') + "-header");
	let numberOfEntries = swimmerDiv.textContent.split(" ")[3] - 1;
	let points = swimmerDiv.textContent.split(" ")[6];

	swimmerDiv.textContent = `${swimmerName} - ${numberOfEntries} Entries - ${points - eventPoints} Points`
	//wait 1 second before updating the point totals
	setTimeout(updatePointTotals, 1000);
  });
});
