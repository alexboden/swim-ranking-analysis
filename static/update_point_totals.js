// update_point_totals.js
// Make an AJAX call to fetch the latest point totals from the server
function updatePointTotals() {
  fetch('/points_by_team')
    .then(response => response.json())
    .then(data => {
		console.log(data);	
      });
}

// Update the point totals every 10 seconds
setInterval(updatePointTotals, 10000);
