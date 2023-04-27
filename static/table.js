let tableBody = document.querySelector('table tbody');
let table = document.querySelector('table');

const individual_points = {
    1: 20,
    2: 17,
    3: 16,
    4: 15,
    5: 14,
    6: 13,
    7: 12,
    8: 11,
    9: 9,
    10: 7,
    11: 6,
    12: 5,
    13: 4,
    14: 3,
    15: 2,
    16: 1
};

// Move row up
let moveUpButtons = document.querySelectorAll('.btn-move-up');
for (let i = 0; i < moveUpButtons.length; i++) {
    moveUpButtons[i].addEventListener('click', function () {
        let row = this.parentNode.parentNode;
        if (row.previousElementSibling) {
            let prevRow = row.previousElementSibling;
            swapValues(row, prevRow);
            tableBody.insertBefore(row, prevRow);
			let eventId = table.id.slice(0, -6);
			switchSwimmers(eventId, row.cells[1].textContent, prevRow.cells[1].textContent);
			console.log(`Swimmer: ${row.cells[1].textContent}, Event: ${eventId}`);
            console.log(`Swimmer: ${prevRow.cells[1].textContent}, Event: ${eventId}`);
		}
    });
}

// Move row down
let moveDownButtons = document.querySelectorAll('.btn-move-down');
for (let i = 0; i < moveDownButtons.length; i++) {
    moveDownButtons[i].addEventListener('click', function () {
        let row = this.parentNode.parentNode;
        if (row.nextElementSibling) {
            let nextRow = row.nextElementSibling;
            swapValues(row, nextRow);
            tableBody.insertBefore(nextRow, row);
			let eventId = table.id.slice(0, -6);
			switchSwimmers(eventId, nextRow.cells[1].textContent, row.cells[1].textContent);
        }
    });
}

// Function to swap ranking and points values between two rows
function swapValues(row1, row2) {
    let tempRanking = row1.querySelector('td:nth-child(1)').textContent;
    let tempPoints = row1.querySelector('td:nth-child(5)').textContent;
    row1.querySelector('td:nth-child(1)').textContent = row2.querySelector('td:nth-child(1)').textContent;
    row1.querySelector('td:nth-child(5)').textContent = row2.querySelector('td:nth-child(5)').textContent;
    row2.querySelector('td:nth-child(1)').textContent = tempRanking;
    row2.querySelector('td:nth-child(5)').textContent = tempPoints;
}

// Delete row
let deleteButtons = document.querySelectorAll('.btn-delete');
for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener('click', function () {
        let row = this.parentNode.parentNode;
        let tableBody = row.parentNode;
        let eventId = table.id.slice(0, -6);
        let swimmerName = row.cells[1].textContent;
        row.parentNode.removeChild(row);

        // Update ranking and points for remaining rows
        let rows = tableBody.rows;
        for (let j = 0; j < rows.length; j++) {
            let currentRank = j + 1;
			let currentPoints = 0;

            if(currentRank <= Object.keys(individual_points).length) {
				currentPoints = individual_points[currentRank];
			}
			// currentPoints = 0;
            rows[j].cells[0].textContent = currentRank;
            rows[j].cells[4].textContent = currentPoints;

            // Update database with new ranking and points
            let swimmerName = rows[j].cells[1].textContent;
			console.log(`currentPoints: ${currentPoints}, currentRank: ${currentRank}, swimmerName: ${swimmerName}, eventId: ${eventId}`)
            updateSwimmerEvent(eventId, swimmerName, currentRank, currentPoints);
        }

        // Delete swimmer from database
        deleteSwimmerEvent(eventId, swimmerName);
    });
}


// Makes API call to switch swimmers
function switchSwimmers(event, name1, name2) {
  fetch('/swap_swimmers', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      event: event,
      name1: name1,
      name2: name2
    })
  })
  .then(response => {
    if (response.ok) {
      // Handle successful response here
      console.log('Swimmers switched successfully!');
    } else {
      // Handle error response here
      console.error('Error switching swimmers:', response.statusText);
    }
  })
  .catch(error => {
    // Handle network error here
    console.error('Network error:', error);
  });
}

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

function updateSwimmerEvent(event, name, rank, points) {
	fetch('/update_swimmer', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			event : event,
			name : name,
			rank : rank,
			points : points,
		})
	})
	.then(response => {
		if (response.ok) {
			// Handle successful response here
			console.log('Swimmer updated successfully!');
		} else {
			// Handle error response here
			console.error('Error updating swimmer:', response.statusText);
		}
	})
	.catch(error => {
		// Handle network error here
		console.error('Network error:', error);
	});
}

