window.onload = function () {
    const keywordTable = document.getElementById('keyword-table-body');
    getKeywords(keywordTable)
}

function getKeywords(e) {
    $.ajax({
        type: 'GET',
        url: '/accounts/load-keywords/',
        success: function (response) {
            const data = response.data
            if(data.length == 0) {
                e.innerHTML += `
                    <p>Nothing added yet!</p>
                `
            }
            data.forEach(element => {
                e.innerHTML += `
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
            console.log(error)
        }
    })
}

function deleteKeyword(button) {
    if(confirm("Are you sure want to delete this item?") == false) {
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
        success: function(response) {
            console.log(response.data)
            tr.parentNode.removeChild(tr);
        },
        error: function(error) {
            console.log('Error: ', error);
        }

    });
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



