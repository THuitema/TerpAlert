/**
 * Constants for placeholder animation
 */
let i = 0;
let placeholder = "";
const txt = "Old Fashioned Texas Fried Chicken";
let speed = 45;
let cursorOn = false;
// let menu = [];

// Return list of menu item names for the autocomplete in search
// async function loadMenu() {
//     try {
//         const response = await fetch('/api/v1/items/?' + new URLSearchParams({all: 'True'}).toString());
//         const data = await response.json();
//
//         // Return list of menu item names
//         const names = data.map(item => item.name);
//         return names;
//     } catch (error) {
//         console.error('Error fetching menu:', error);
//         return []; // Return an empty array on error
//     }
// }

/**
 * Apply autocomplete functionality to search bar
 */
window.onload = function () {
    // Cache menu for autocomplete to use and create autocomplete
    // (async function () {
    //     try {
    //         menu = await loadMenu(); // Call your async function
    //         console.log(menu); // Do something with the result
    //     } catch (error) {
    //         menu = []
    //         console.error(error); // Handle any errors
    //     }
    //
    //
    // })();
    // Autocomplete
    console.log('Initializing autocomplete...');
    initializeAutocomplete();
    // loadMenu()
    //     .then(() => {
    //         console.log('Menu:', menu);
    //         initializeAutocomplete();
    //     })
    //     .catch(error => {
    //         console.log('Failed to initialize autocomplete:', error)
    //     });

    console.log('Done initializing autocomplete uhhh...');

    // Animate search bar placeholder
    animatePlaceholder();
}

function initializeAutocomplete() {
    $('#food-input').autocomplete({
        source: function (request, response) {
            // You can fetch data from your server using AJAX or use a static array
            $.ajax({
                url: '/api/v1/items/?' + new URLSearchParams({count: '10', term: request.term}).toString(),
                dataType: 'json', // Expected response type
                success: function (data) {
                    let menu = data.map(item => item.name);
                    console.log('Menu data loaded successfully', menu)
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

// function loadMenu(request, response) {
//     // try {
//     //     const response = await fetch('/api/v1/items/?' + new URLSearchParams({all: 'True'}).toString());
//     //     const data = await response.json();
//     //
//     //     // Return list of menu item names
//     //     const names = data.map(item => item.name);
//     //     return names;
//     // } catch (error) {
//     //     console.error('Error fetching menu:', error);
//     //     return []; // Return an empty array on error
//     // }
//
//     fetch('/api/v1/items/?' + new URLSearchParams({count: '10', term: request.term}).toString())
//         .then(response => response.json())
//         .then(data => {
//             let menu = data.map(item => item.name);
//             console.log('Menu data loaded successfully', menu)
//             response(menu);
//         })
//         .catch(error => {
//             console.error('Error loading menu data:', error);
//             response(error);
//         });
//
// }

// Preload data when the page loads
// window.addEventListener('load', () => {
//     loadMenu();
// });

// /**
//  * Sends an Ajax request to get relevant menu items based on the search term
//  * @param request Contains the search term from the user
//  * @param response Callback function to send labels and values to the autocomplete menu
//  */
// function getMenu(request, response) {
//     return $.ajax({
//         type: 'GET',
//         url: '/api/v1/items/',
//         data: {
//             'term': request.term,
//         },
//         success: function (data) {
//             console.log("value:", "key:");
//             let results = $.map(data.results, function (value, key) {
//                 return {
//                     label: value.name,
//                     value: value.name
//                 }
//             });
//             response(results.slice(0, 10)); // limit to 10 results
//         }
//     })
// }

/**
 * Sends an Ajax request to check if item is being served today, and renders the appropriate response
 * @param input Search term
 */
function checkAlertExists(input) {
    $.ajax({
        type: 'GET',
        url: '/api/v1/daily-items/',  //'/check-for-alert',
        data: {
            'name': input,
        },
        success: function (data) {
            results = data.results

            $('#food-input').val('');
            $('#food-input').attr('placeholder', '')
            const result = document.getElementById('food-input-results') // $('#food-input-results');
            console.log(results);
            if (results.length == 1) { // data.found == true
                var dining_halls = [];
                if (results[0].dh_south) {
                    dining_halls.push("South")
                }
                if (results[0].dh_251) {
                    dining_halls.push("251")
                }
                if (results[0].dh_y) {
                    dining_halls.push("Yahentamitsi")
                }
                result.innerHTML = '🚨 ' + input + ' is being served at ' + dining_halls.join(', ') + ' 🚨';
            } else { // Item is not being served today
                result.innerHTML = "Sorry, no dining halls have " + input + " today"; // data.item
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
