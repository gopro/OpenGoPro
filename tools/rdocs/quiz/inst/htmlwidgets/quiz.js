/* quiz.js/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Thu, May  6, 2021 11:38:41 AM */

HTMLWidgets.widget({
    name: 'quiz',

    type: 'output',

    factory: function (el, width, height) {
        const output = [];
        const answers = [];

        return {
            renderValue: function (x) {
                function buildQuiz() {
                    // For each available answer...
                    x.answers.forEach(function (answer) {
                        // ...add an HTML radio button
                        answers.push(
                            `<label>
                                <input type="radio" name="question" value="${answer[0]}">
                                ${answer[0]} :
                                ${answer[1]}
                            </label>
                            <br>`
                        );
                    });

                    // add this question and its answers to the output
                    output.push(
                        `<div>
                            <div class="question"> ${x.question} </div>
                            <div class="answers"> ${answers.join('')} </div>
                        </div>`
                    );
                    // Add the submit button
                    output.push(
                        `<button id="submit${x.question}">Submit Answer</button>`
                    );
                    // Add the results div
                    output.push(`<div id="results_info${x.question}"></div>`);
                    // Add a new line
                    output.push(`<br>`);

                    // finally combine our output list into one string of HTML and put it on the page
                    el.innerHTML = output.join('');
                }

                function showResults() {
                    // gather answer containers from our quiz
                    const answerContainers = el.querySelectorAll('.answers');
                    const answerContainer = answerContainers[0];
                    const selector = `input:checked`;
                    const userAnswer = answerContainer.querySelector(selector) || {};

                    // if answer is correct
                    if (userAnswer.value === x.correct_answer) {
                        // color the answers green
                        answerContainer.style.color = 'green';
                        resultsContainer.innerHTML = `<div>
                                Correct!! 😃 ${x.answer_info}
                            </div>`;
                    }
                    // if answer is wrong or blank
                    else {
                        // color the answers red
                        answerContainer.style.color = 'red';
                        resultsContainer.innerHTML = `<div>
                            Incorrect!! 😭 ${x.answer_info}
                        </div>`;
                    }
                }

                buildQuiz();

                const resultsContainer = document.getElementById(
                    'results_info' + x.question
                );
                const submitButton = document.getElementById('submit' + x.question);

                // Set up event listeners
                submitButton.addEventListener('click', showResults);
            },

            resize: function (width, height) {
                // TODO: code to re-render the widget with a new size
            },
        };
    },
});
