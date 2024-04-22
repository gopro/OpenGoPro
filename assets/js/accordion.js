window.addEventListener('load', function () {
    const accordions = document.getElementsByClassName('accordion');

    Array.prototype.forEach.call(accordions, function (link) {
        link.addEventListener(
            'click',
            function (event) {
                /* Toggle between adding and removing the "active" class,
                to highlight the button that controls the panel */
                this.classList.toggle('accordion-active');
                var arrow = this.getElementsByTagName('i')[0];
                arrow.classList.toggle('fa-chevron-down');
                arrow.classList.toggle('fa-chevron-up');

                /* Toggle between hiding and showing the active panel */
                var panel = this.nextElementSibling;
                if (panel.style.display === 'block') {
                    panel.style.display = 'none';
                } else {
                    panel.style.display = 'block';
                }
            },
            false
        );
    });
});
