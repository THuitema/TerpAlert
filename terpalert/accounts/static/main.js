let alertTableBody;

window.onload = function () {
    alertTableBody = document.getElementById('alert-table-body');
    getAlerts();
}

function getAlerts() {
    $.ajax({
        type: 'GET',
        url: '/accounts/load-alerts/',
        success: function (response) {
            const data = response.data;
            if (data.length == 0) {
                alertTableBody.innerHTML = `
                    <p>Nothing added yet!</p>
                `
            }
            data.forEach(element => {
                console.log(element)
                alertTableBody.innerHTML += `
                    <tr data-alert-id="${element.id}">
                        
                        <td>${element.alert}</td>
                        <td>
                            <button type="button" class="btn btn-danger" onclick="this.blur(); deleteAlert(this);">
                                <i class="bi bi-trash"></i>
                            </button>
                        </td>
                        
                    </tr>
                `
            });
        },
        error: function (error) {
            console.log(error);
        }
    })
}

function deleteAlert(button) {
    if (confirm("Are you sure want to delete this alert?") == false) {
        return;
    }

    const csrftoken = getCookie('csrftoken');
    const td = button.parentNode;
    const tr = td.parentNode;

    $.ajax({
        type: 'POST',
        url: '/accounts/delete-alert/',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'alert-id': tr.getAttribute('data-alert-id'),
        },
        success: function (response) {
            console.log(response.data)
            tr.parentNode.removeChild(tr);
        },
        error: function (error) {
            console.log('Error: ', error);
        }

    });
}

function addAlert(button) {
    button.disabled = true; // don't allow button to be clicked until the form is saved or cancelled

    const table = document.getElementById('alert-table');
    const row = table.insertRow(1);
    const cell1 = row.insertCell(0);
    const cell2 = row.insertCell(1);

    cell1.innerHTML = `
        <input type="text" name="alert" id="alert-input" placeholder="Type here" required>
    `;
    cell2.innerHTML = `
        <button type="button" class="btn btn-light rounded-circle" onclick="cancelRow(this);">
            <i class="bi bi-x-circle"></i>
        </button>
        <button type="button" class="btn btn-success rounded-circle" id="save-btn" onclick="saveAlert(this);" disabled>
            <i class="bi bi-check2-circle"></i>
        </button>
    `;

    $('#keyword-input').on('keyup', checkKeyworkInput);
}

function saveAlert(button) {
    const input = $('#alert-input').val();
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'POST',
        url: '/accounts/save-alert/',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'alert': input
        },
        success: function (response) {
            if (response.success == true) {
                // delete input row and insert new keyword row at top of table
                cancelRow(button);
                const table = document.getElementById('alert-table');
                const row = table.insertRow(1);
                // row.id = response.id;
                row.setAttribute('data-alert-id', response.id)
                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);

                cell1.innerHTML = response.alert;
                cell2.innerHTML = `
                    <button type="button" class="btn btn-danger" onclick="this.blur(); deleteAlert(this);">
                        <i class="bi bi-trash"></i>
                    </button>
                `
            } else {
                alert(response.message);
            }
        },
        error: function (error) {
            alert('Something went wrong, please try again later');
        }
    });
}

function cancelRow(button) {
    const tr = button.parentNode.parentNode;
    tr.parentNode.removeChild(tr);
    document.getElementById('add-button').disabled = false;
}

function checkKeyworkInput() {
    if ($('#alert-input').val().length > 0) {
        $('#save-btn').prop('disabled', false);
    } else {
        $('#save-btn').prop('disabled', true);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



