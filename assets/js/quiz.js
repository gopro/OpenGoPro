/* quiz.js/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed, Sep  1, 2021  5:06:15 PM */

function showResults(uuid, correct) {
    const answers_id = 'answers_' + uuid;
    const results_id = 'results_' + uuid;
    const correct_id = 'correct_' + uuid;
    const incorrect_id = 'incorrect_' + uuid;

    const answersContainer = document.getElementById(answers_id);
    const resultsContainer = document.getElementById(results_id);
    const correctContainer = document.getElementById(correct_id);
    const incorrectContainer = document.getElementById(incorrect_id);

    const selector = `input:checked`;
    const userAnswer = answersContainer.querySelector(selector) || {};

    // Show results
    resultsContainer.style.display = 'block';

    // if answer is correct
    if (userAnswer.value === correct) {
        // color the answers green
        answersContainer.style.color = 'green';
        correctContainer.style.display = 'block';
        incorrectContainer.style.display = 'none';
    }
    // if answer is wrong or blank
    else {
        // color the answers red
        answersContainer.style.color = 'red';
        correctContainer.style.display = 'none';
        incorrectContainer.style.display = 'block';
    }
}
