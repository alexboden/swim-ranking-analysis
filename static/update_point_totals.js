// update_point_totals.js
// Make an AJAX call to fetch the latest point totals from the server
function updatePointTotals() {
  fetch('/points_by_team')
    .then(response => response.json())
    .then(data => {
		for (key in data) {
			document.querySelector(`#team-points-${key.split(" ")[0]}`).innerHTML = `${key}: ${data[key]}`;
		}
      });
}

// Update the point totals every 10 seconds
// setInterval(updatePointTotals, 10000);
