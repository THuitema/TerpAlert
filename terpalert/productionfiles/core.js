/**
 * Constants for placeholder animation
 */
let i = 0;
let placeholder = "";
const txt = "Old Fashioned Texas Fried Chicken";
let speed = 45;
let cursorOn = false;

/**
 * Apply autocomplete functionality to search bar
 */
window.onload = function () {
    initializeAutocomplete();
    animatePlaceholder();
}

function initializeAutocomplete() {
    $('#food-input').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: '/api/v1/items/?' + new URLSearchParams({count: '10', term: request.term}).toString(),
                dataType: 'json',
                success: function (data) {
                    let menu = data.map(item => item.name);
                    response(menu);
                }
            });
        },
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
        // Check if item is being served today, when selected
        select: function (event, ui) {
            const input = $('#food-input');
            input.val(ui.item.label);
            checkAlertExists(input.val());
        },
        delay: 200,
        minLength: 1,
    })
}

/**
 * Sends an Ajax request to check if item is being served today, and renders the appropriate response
 * @param input Search term
 */
function checkAlertExists(input) {
    $.ajax({
        type: 'GET',
        url: '/api/v1/daily-items',
        data: {
            'match_name': input,
        },
        success: function (data) {
            let results = data.results

            $('#food-input').val('');
            $('#food-input').attr('placeholder', '')
            const result = document.getElementById('food-input-results')

            let dh_south = false;
            let dh_251 = false;
            let dh_y = false;

            if (results.length == 1) {
                if (results[0].dh_south) {
                    dh_south = true;
                }
                if (results[0].dh_251) {
                    dh_251 = true;
                }
                if (results[0].dh_y) {
                    dh_y = true;
                }
            }

            // Build output showing status at each dining hall
            let result_html = `<h4>${input}</h4>`;
            let dh_status = ''
            dh_status = 'Yahentamitsi' + ((dh_y) ? ' ✅ ' : ' ❌ ');
            dh_status += '  South' + ((dh_south) ? ' ✅ ' : ' ❌ ');
            dh_status += '  251' + ((dh_251) ? ' ✅ ' : ' ❌ ');
            result.innerHTML = result_html + `<p>${dh_status}</p>`;

            // if (results.length == 1) { // data.found == true
            //     var dining_halls = [];
            //     if (results[0].dh_south) {
            //         dining_halls.push("South")
            //     }
            //     if (results[0].dh_251) {
            //         dining_halls.push("251")
            //     }
            //     if (results[0].dh_y) {
            //         dining_halls.push("Yahentamitsi")
            //     }
            //     result.innerHTML = '🚨 ' + input + ' is being served at ' + dining_halls.join(', ') + ' 🚨';
            // } else { // Item is not being served today
            //     result.innerHTML = "Sorry, no dining halls have " + input + " today"; // data.item
            //     result.classList.add('auth-form-error')
            // }
        },
        error: function (error) {
            alert('Something went wrong, please try again later');
        }
    })
}

/**
 * Animate the placeholder of food search bar by "typing" an example phrase
 */
function animatePlaceholder() {
    // only show animation before user types any input
    if ($('#food-input').val() === '') {
        // "typing" the placeholder out
        if (i < txt.length) {
            placeholder += txt.charAt(i);
            i++;
        }
        // after "typing", show a blinking cursor after
        else {
            speed = 420;
            if (cursorOn == true) {
                placeholder = placeholder.substring(0, placeholder.length - 1);
                cursorOn = false;
            } else {
                placeholder += '|';
                cursorOn = true;
            }
        }
        document.getElementById('food-input').setAttribute('placeholder', placeholder);
        setTimeout(animatePlaceholder, speed)
    }
}
