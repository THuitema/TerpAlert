window.onload = function () {
    const box = document.getElementById('keyword-box');
    getKeywords(box)
}


function getKeywords(div) {
    $.ajax({
        type: 'GET',
        url: '/accounts/load-keywords/',
        success: function(response) {
            console.log(response.data)
            const data = response.data
            data.forEach(element => {
                div.innerHTML += `
                    <div class="keyword" id="${element.id}">${element.keyword}</div>
             
                `
                // ${element.user}
            });


        },
        error: function(error) {
            console.log(error)

        }
    })
}



