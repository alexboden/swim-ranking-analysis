let table = document.querySelector('table tbody');

// Move row up
let moveUpButtons = document.querySelectorAll('.btn-move-up');
for (let i = 0; i < moveUpButtons.length; i++) {
    moveUpButtons[i].addEventListener('click', function () {
        let row = this.parentNode.parentNode;
        let table = row.parentNode;
        if (row.previousElementSibling) {
            table.insertBefore(row, row.previousElementSibling);
        }
    });
}

// Move row down
let moveDownButtons = document.querySelectorAll('.btn-move-down');
for (let i = 0; i < moveDownButtons.length; i++) {
    moveDownButtons[i].addEventListener('click', function () {
        let row = this.parentNode.parentNode;
        let table = row.parentNode;
        if (row.nextElementSibling) {
            table.insertBefore(row.nextElementSibling, row);
        }
    });
}

// Delete row
let deleteButtons = document.querySelectorAll('.btn-delete');
for (let i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener('click', function () {
        let row = this.parentNode.parentNode;
        row.parentNode.removeChild(row);
    });
}
