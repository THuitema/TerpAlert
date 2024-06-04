let alertTableBody;

/**
 * When the window is loaded, display the user's alerts in a table
 */
window.onload = function () {
    alertTableBody = document.getElementById('alert-table-body');
    if (alertTableBody != null) {
        getAlerts();
    }

    // Delete alert confirmation dialogue
    const deleteModal = document.getElementById('delete-modal');
    if (deleteModal) {
        let button;
        deleteModal.addEventListener('show.bs.modal', event => {
            button = event.relatedTarget;
            const modalBody = deleteModal.querySelector('.modal-body');
            const alert = button.getAttribute('data-bs-alert');
            modalBody.textContent = `Are you sure you want to delete "${alert}"?`;
        });

        const deleteBtn = deleteModal.querySelector('.btn-danger');
        deleteBtn.addEventListener('click', e => {
            button.blur();
            deleteAlert(button);
        });
    }

    // Alert already exists popup modal
    $('#already-exists-modal').modal({ show: false})

    // Alert notification button animation - shake when page loads
    const alertNotificationBtn = document.getElementById('show-notifications-button')
    if(alertNotificationBtn != null) {
        alertNotificationBtn.classList.add('apply-shake')
    }
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
            alertTableBody.innerHTML = '';
            data.forEach(alert => {
                alertTableBody.innerHTML += `
                    <tr data-alert-id="${alert.id}">
                        <!-- Cell 1 contains the alert -->
                        <td>${alert.alert}</td>
                        <!-- Cell 2 contains the delete button -->
                        <td class="col-right">
                            <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" 
                            data-bs-target="#delete-modal" data-bs-alert="${alert.alert}">
                                <i class="bi bi-trash3-fill"></i>
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
    document.getElementsByName('add-button').forEach(btn => {
        btn.disabled = true;
    });

    const row = alertTableBody.insertRow(0);
    const cell1 = row.insertCell(0);
    const cell2 = row.insertCell(1);

    row.id = 'input-row';

    // cell1 contains the input field for the new alert
    cell1.innerHTML = `
        <input type="text" class="form-control no-border shadow-none input-width" name="alert" id="alert-input" 
        placeholder="Type here" required>
    `;

    // cell2 contains the cancel button
    cell2.innerHTML = `
        <button type="button" class="btn rounded-circle" style="background-color: transparent;"
         onclick="removeInputRow();">
            <i class="bi bi-x-circle"></i>
        </button>
    `;
    cell2.className = 'col-right'

    // set focus to input text box
    document.getElementById('alert-input').focus();

    // Autocomplete dropdown for input
    $('#alert-input').autocomplete({
        // Sends an Ajax request to gather menu items matching user's input
        source: getMenu,
        // Bold characters in results that match search term (case-insensitive)
        open: function (event, ui) {
            const data = $(this).data('ui-autocomplete');
            data.menu.element.find('li').each(function () {
                const me = $(this);
                const keywords = data.term.split(' ').join('|');
                let textWrapper = me.find('.ui-menu-item-wrapper');
                let text = textWrapper.text();
                let newTextHtml = text.replace(new RegExp("(" + keywords + ")", "gi"), '<b>$1</b>');
                textWrapper.html(newTextHtml);
            });
        },
        // Save item when selected
        select: function (event, ui) {
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
                getAlerts();
            } else {
                // invalid submission occurred
                $('#already-exists-modal').modal('show');
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
    document.getElementsByName('add-button').forEach(btn => {
        btn.disabled = false;
    });
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

/**
 * Formats a raw phone number to (XXX) XXX-XXXX
 * @param value Raw phone number typed by user
 * @returns {*|string} Formatted phone number
 */
function formatPhoneNumber(value) {
    if (!value) {
        return value
    }
    const phoneNumber = value.replace(/\D/g, ''); // /[^/d]/g
    const length = phoneNumber.length;
    if (length < 4) {
        return phoneNumber;
    }
    if (length < 7) {
        return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3)}`;
    }
    return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(
        3,
        6,
    )}-${phoneNumber.slice(6, 10)}`;
}

/**
 * Formats phone number as user is typing
 * Retrieves raw phone number from HTML element with id 'id_phone'
 */
function phoneNumberFormatter() {
    const phoneInput = document.getElementById('id_phone');
    phoneInput.value = formatPhoneNumber(phoneInput.value);
}
