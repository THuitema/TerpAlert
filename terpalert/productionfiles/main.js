window.onload = function () {
    const navLinks = document.querySelectorAll('.nav-item');
    const menuToggle = document.getElementById('main-nav');
    const collapse = bootstrap.Collapse.getOrCreateInstance(menuToggle, {toggle: false});

    // Close navbar menu after a link is clicked
    navLinks.forEach((l) => {
        l.addEventListener('click', () => {
            collapse.toggle()
        })
    })
}