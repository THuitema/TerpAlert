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
    // Autocomplete
    $('#food-input').autocomplete({
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
        // Check if item is being served today, when selected
        select: function (event, ui) {
            const input = $('#food-input');
            input.val(ui.item.label);
            checkAlertExists(input.val());
        },
        delay: 200,
        minLength: 1,
    })

    // Animate search bar placeholder
    animatePlaceholder();
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
 * Sends an Ajax request to check if item is being served today, and renders the appropriate response
 * @param input Search term
 */
function checkAlertExists(input) {
    $.ajax({
        type: 'GET',
        url: '/check-for-alert',
        data: {
            'item': input,
        },
        success: function (data) {
            $('#food-input').val('');
            $('#food-input').attr('placeholder', '')
            const result = document.getElementById('food-input-results') // $('#food-input-results');

            if (data.found == true) { // Item is being served today
                result.innerHTML = '🚨 ' + data.item + ' is being served at ' + data.dining_halls + ' 🚨';
            } else { // Item is not being served today
                result.innerHTML = "Sorry, no dining halls have " + data.item + " today";
                result.classList.add('auth-form-error')
            }
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
