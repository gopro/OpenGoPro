/* tabs.js/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  1, 2021  5:06:15 PM */

const removeActiveClasses = function (ulElement) {
    const lis = ulElement.querySelectorAll('li');
    Array.prototype.forEach.call(lis, function (li) {
        li.classList.remove('active');
    });
};

const getChildPosition = function (element) {
    var parent = element.parentNode;
    var i = 0;
    for (var i = 0; i < parent.children.length; i++) {
        if (parent.children[i] === element) {
            return i;
        }
    }

    throw new Error('No parent found');
};

const isLinked = function (link) {
    liTab = link.parentNode;
    ulTab = liTab.parentNode;
    return ulTab.classList.contains('tab-linked');
};

/**
 * Given the hyperlink of the selected tab, update the tab and and tab content
 *
 * @param {*} link
 * @returns
 */
const updateTabFromLink = function (link) {
    liTab = link.parentNode;

    if (liTab.className.includes('active')) {
        return;
    }

    ulTab = liTab.parentNode;
    position = getChildPosition(liTab);

    updateTabContainer(ulTab, position);

    return position;
};

/**
 * Given tab container and postiion of target active element, make target tab and tab content active
 *
 * @param {*} ulTab
 * @param {*} position
 */
const updateTabContainer = function (ulTab, position) {
    // Remove active classes from tab headers
    removeActiveClasses(ulTab);
    tabContentId = ulTab.getAttribute('data-tab');
    // Get tab content (both active and inactive)
    tabContentElement = document.getElementById(tabContentId);
    removeActiveClasses(tabContentElement);

    // Make the target position tab content active
    tabContentElement
        .querySelectorAll('.tab-content-container')
        [position].classList.add('active');
    // Get the target tab
    liTab = ulTab.querySelectorAll('li')[position];
    liTab.classList.add('active');
};

window.addEventListener('load', function () {
    const tabLinks = document.querySelectorAll('ul.tab li a');

    Array.prototype.forEach.call(tabLinks, function (link) {
        link.addEventListener(
            'click',
            function (event) {
                event.preventDefault();

                activePosition = updateTabFromLink(link);

                // If this is a linked tab, update other linked tabs
                if (isLinked(link)) {
                    document.querySelectorAll('.tab-linked').forEach(function (ulTab) {
                        updateTabContainer(ulTab, activePosition);
                    });
                }
            },
            false
        );
    });
});
