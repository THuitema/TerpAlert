let alertTableBody;

/**
 * When the window is loaded, display the user's alerts in a table
 */
window.onload = function () {
    alertTableBody = document.getElementById('alert-table-body');
    getAlerts();
}

/**
 * Send an Ajax request to retrieve the user's alerts,
 * then display each one in a table row
 */
function getAlerts() {
    $.ajax({
        type: 'GET',
        url: '/accounts/load-alerts/',
        success: function (response) {
            const data = response.data;

            // Display each alert in a row in the table
            data.forEach(alert => {
                alertTableBody.innerHTML += `
                    <tr data-alert-id="${alert.id}">
                        <!-- Cell 1 contains the alert -->
                        <td>${alert.alert}</td>
                        <!-- Cell 2 contains the delete button -->
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
            alert('Something went wrong, please try again later');
        }
    })
}

/**
 * Sends an Ajax request to delete the specified alert
 * @param button Button clicked to delete alert
 */
function deleteAlert(button) {
    // Show popup for user to confirm they want to delete alert
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
        data: { // sends the id of the alert
            'alert-id': tr.getAttribute('data-alert-id'),
        },
        success: function (response) {
            tr.parentNode.removeChild(tr); // delete row from html
        },
        error: function (error) {
            alert('Something went wrong, please try again later');
        }
    });
}

/**
 * Adds row to top of table allowing the user to enter a new alert and save it
 * @param button Button clicked to add alert
 */
function addAlert(button) {
    button.disabled = true; // don't allow the add button to be clicked until the new alert is saved or cancelled

    const table = document.getElementById('alert-table');
    const row = table.insertRow(1);
    const cell1 = row.insertCell(0);
    const cell2 = row.insertCell(1);

    row.id = 'input-row';

    // cell1 contains the input field for the new alert
    cell1.innerHTML = `
        <input type="text" name="alert" id="alert-input" placeholder="Type here" required>
    `;

    // cell2 contains the cancel button
    cell2.innerHTML = `
        <button type="button" class="btn btn-light rounded-circle" onclick="removeInputRow();">
            <i class="bi bi-x-circle"></i>
        </button>
    `;

    // Autocomplete dropdown for input
    $('#alert-input').autocomplete({
        // Sends an Ajax request to gather menu items matching user's input
        source: getMenu,
        select: function (event, ui) { // save selection
            $('#alert-input').val(ui.item.label);
            saveAlert($('#save-btn'));
        },
        delay: 200,
        minLength: 1,
    });
}

/**
 * Sends an Ajax request to get relevant menu items based on the search term
 * @param request Contains the search term from the user
 * @param response Callback function to send labels and values to the autocomplete menu
 */
function getMenu(request, response) {
    return $.ajax({
        type: 'GET',
        url: '/accounts/load-menu/',
        data: {
            'term': request.term,
        },
        success: function (data) {
            let results = $.map(data.data, function (value, key) {
                return {
                    label: value.label, // label and value is the name of the menu item
                    value: value.label
                }
            });
            response(results.slice(0, 10)); // limit to 10 results
        }
    })
}

/**
 * Sends an Ajax request to save the alert entered by the user
 */
function saveAlert() {
    const input = $('#alert-input').val(); // alert entered by user
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'POST',
        url: '/accounts/save-alert/',
        headers: {'X-CSRFToken': csrftoken},
        data: { // sends the alert name
            'alert': input
        },
        success: function (response) {
            if (response.success == true) {
                // delete input row and insert new alert row at top of table
                removeInputRow();
                const table = document.getElementById('alert-table');
                const row = table.insertRow(1);
                row.setAttribute('data-alert-id', response.id)
                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);

                // cell1 contains the alert
                cell1.innerHTML = response.alert;
                // cell2 contains the delete button
                cell2.innerHTML = `
                    <button type="button" class="btn btn-danger" onclick="this.blur(); deleteAlert(this);">
                        <i class="bi bi-trash"></i>
                    </button>
                `
            } else {
                // invalid submission occurred
                alert(response.message);
                $('#alert-input').val('') // clear input field after invalid submission
            }
        },
        error: function (error) {
            alert('Something went wrong, please try again later');
        }
    });
}

/**
 * Removes alert input row and reenables the add alert button
 */
function removeInputRow() {
    $('#input-row').remove();
    document.getElementById('add-button').disabled = false;
}

/**
 * Django-provided function to retrieve a cookie
 * @param name Name of cookie to get
 * @returns Value of cookie
 */
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
