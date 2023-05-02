let toggleButtons = document.querySelectorAll('[data-table-id]');

for (let i = 0; i < toggleButtons.length; i++) {
    toggleButtons[i].addEventListener('click', function() {
        let tableId = toggleButtons[i].getAttribute('data-table-id');
        let table = document.getElementById(tableId.replace(' ', '') + '-table');
        if (table.style.display === 'none') {
            table.style.display = 'table';
        } else {
            table.style.display = 'none';
        }
    });
}


let team_toggle_collapse_buttons = document.querySelectorAll('#btn-collapse-team');
for (let i = 0; i < team_toggle_collapse_buttons.length; i++) {
    team_toggle_collapse_buttons[i].addEventListener('click', function() {
        let teamId = team_toggle_collapse_buttons[i].getAttribute('team-id');
		teamId = teamId.split(' ')[0];
		console.log(teamId)
        let div = document.getElementById('team-div-' + teamId);
		console.log(div)
		div.style.display = 'none';
    });
}



let team_toggle_expand_buttons = document.querySelectorAll('#btn-expand-team');
for (let i = 0; i < team_toggle_expand_buttons.length; i++) {
    team_toggle_expand_buttons[i].addEventListener('click', function() {
        let teamId = team_toggle_expand_buttons[i].getAttribute('team-id');
		teamId = teamId.split(' ')[0];
		console.log(teamId)
        let div = document.getElementById('team-div-' + teamId);
		console.log(div)
		div.style.display = 'block';
    });
}

document.getElementById('btn-collapse-all-team').addEventListener('click', function () {
	// Loop through all the tables and set their display property to "none"
	console.log('test')
	for (let i = 0; i < team_toggle_collapse_buttons.length; i++) {
        let teamId = team_toggle_collapse_buttons[i].getAttribute('team-id');
        teamId = teamId.split(' ')[0];
        let div = document.getElementById('team-div-' + teamId);
		div.style.display = 'none';
	}
});
