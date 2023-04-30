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
