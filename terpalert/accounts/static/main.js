window.onload = function () {
    const keywordTable = document.getElementById('keyword-table-body');
    getKeywords(keywordTable)
}

function getKeywords(e) {
    $.ajax({
        type: 'GET',
        url: '/accounts/load-keywords/',
        success: function (response) {
            console.log(response.data)
            const data = response.data
            data.forEach(element => {
                e.innerHTML += `
                    <tr id="${element.id}">
                        <td>${element.keyword}</td>
                        <td><i class="bi bi-trash"></i></td>
                    </tr>
                `
                // ${element.user}
            });

        },
        error: function (error) {
            console.log(error)
        }
    })
}



