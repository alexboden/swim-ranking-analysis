// Get the buttons
const menButton = document.querySelector('#btn-men');
const womenButton = document.querySelector('#btn-women');

// Add event listeners
menButton.addEventListener('click', () => {
  // Update gender in database
  fetch('/update_gender', {
    method: 'POST',
    body: JSON.stringify({ gender: 'Men' }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(() => {
    // Refresh the page
    location.reload();
  });
});

womenButton.addEventListener('click', () => {
  // Update gender in database
  fetch('/update_gender', {
    method: 'POST',
    body: JSON.stringify({ gender: 'Women' }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(() => {
    // Refresh the page
    location.reload();
  });
});

const entryButton = document.querySelector('#btn-entry');

entryButton.addEventListener('click', () => {
  // Get the form data
  const event = document.querySelector('#event').value;
  const name = document.querySelector('#name').value;
  const seedTime = document.querySelector('#seed-time').value;
  const teamName = document.querySelector('#team-name').value;
  const points = document.querySelector('#points').value;
  const ranking = document.querySelector('#ranking').value;

  // Send the form data to the server
  fetch('/add_entry', {
    method: 'POST',
    body: JSON.stringify({
      event_name: event,
      name: name,
      seed_time: seedTime,
      team_name: teamName,
      points: points,
      ranking: ranking
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(() => {
    // Refresh the page
    location.reload();
  });
});
