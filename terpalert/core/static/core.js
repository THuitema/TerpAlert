window.onload = function () {
    // const searchInput = document.getElementById()
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
        // Save item when selected
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

function checkAlertExists(input) {
    $.ajax({
        type: 'GET',
        url: '/check-for-alert',
        data: {
            'item': input,
        },
        success: function (data) {
            $('#food-input').val('');
            const result = document.getElementById('food-input-results') // $('#food-input-results');

            if (data.found == true) {
                result.innerHTML = '🚨 ' + data.item + ' is being served at ' + data.dining_halls + ' 🚨';
            } else {
                result.innerHTML = "Sorry, " + data.item + " isn't being served today";
            }
        }
    })
}