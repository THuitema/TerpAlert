let keywordTableBody;

window.onload = function () {
    keywordTableBody = document.getElementById('keyword-table-body');
    getKeywords();
}

function getKeywords() {
    $.ajax({
        type: 'GET',
        url: '/accounts/load-keywords/',
        success: function (response) {
            const data = response.data;
            if (data.length == 0) {
                keywordTableBody.innerHTML = `
                    <p>Nothing added yet!</p>
                `
            }
            data.forEach(element => {
                console.log(element)
                keywordTableBody.innerHTML += `
                    <tr id="${element.id}">
                        
                        <td>${element.keyword}</td>
                        <td>
                            <button type="button" class="btn btn-danger" onclick="this.blur(); deleteKeyword(this);">
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

function deleteKeyword(button) {
    if (confirm("Are you sure want to delete this item?") == false) {
        return;
    }

    const csrftoken = getCookie('csrftoken');
    const td = button.parentNode;
    const tr = td.parentNode;

    $.ajax({
        type: 'POST',
        url: '/accounts/delete-keyword/',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'keyword_id': tr.id,
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

function addKeyword(button) {
    button.disabled = true; // don't allow button to be clicked until the form is saved or cancelled

    const table = document.getElementById('keyword-table');
    const row = table.insertRow(1);
    const cell1 = row.insertCell(0);
    const cell2 = row.insertCell(1);

    cell1.innerHTML = `
        <input type="text" name="keyword" id="keyword-input" placeholder="Type here" required>
    `;
    cell2.innerHTML = `
        <button type="button" class="btn btn-light rounded-circle" onclick="cancelRow(this);">
            <i class="bi bi-x-circle"></i>
        </button>
        <button type="button" class="btn btn-success rounded-circle" id="save-btn" onclick="saveKeyword(this);" disabled>
            <i class="bi bi-check2-circle"></i>
        </button>
    `;

    $('#keyword-input').on('keyup', checkKeyworkInput);
}

function saveKeyword(button) {
    const input = $('#keyword-input').val();
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'POST',
        url: '/accounts/save-keyword/',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'keyword': input
        },
        success: function (response) {
            if (response.success == true) {
                console.log('Keyword: ', response.keyword);
                console.log('ID: ', response.id);

                // delete input row and insert new keyword row at top of table
                cancelRow(button);
                const table = document.getElementById('keyword-table');
                const row = table.insertRow(1);
                row.id = response.id;
                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);

                cell1.innerHTML = response.keyword;
                cell2.innerHTML = `
                    <button type="button" class="btn btn-danger" onclick="this.blur(); deleteKeyword(this);">
                        <i class="bi bi-trash"></i>
                    </button>
                `

            } else {
                alert('Something went wrong, please try again later');
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function cancelRow(button) {
    const tr = button.parentNode.parentNode;
    tr.parentNode.removeChild(tr);
    document.getElementById('add-button').disabled = false;
}

function checkKeyworkInput() {
    if ($('#keyword-input').val().length > 0) {
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



