let tableBody = document.querySelector('table tbody');
let table = document.querySelector('table');

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
        row.parentNode.removeChild(row);
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
