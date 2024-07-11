
console.log("Hello from exercise.js");

document.addEventListener("DOMContentLoaded", function () {

    Array.from(document.querySelectorAll('.exercise.checkbox')).forEach(exercise => {
        exercise.querySelector('.exercise-title').addEventListener('click', function(event) {
            // Reset the exercise
            exercise.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
                checkbox.disabled = false;
            });

            exercise.classList.remove('pass');
            exercise.classList.remove('fail');

            // Hide the solution
            const solution = exercise.querySelector('.solution');
            if (solution) {
                solution.style.display = 'none';
            }
            const hint = exercise.querySelector('.hint');
            if (hint) {
                hint.style.display = 'block';
            }
        });

        Array.from(exercise.getElementsByClassName('exercise-list')).forEach(ul => {

            // Multiple choice questions
            ul.addEventListener('change', function (event) {
                if (event.target && event.target.matches('input[type="checkbox"]')) {
                    const isGood = event.target.classList.contains('good');
                    if (isGood) {
                        // If all checkboxes with class 'good' are checked, we associate class `pass` to the parent .admonition.exercise
                        const allGoodCheckboxes = ul.querySelectorAll('input.good');
                        const allGoodCheckboxesChecked = ul.querySelectorAll('input.good:checked');
                        if (allGoodCheckboxes.length === allGoodCheckboxesChecked.length) {
                            ul.parentElement.classList.add('pass');
                            ul.querySelectorAll('input[type="checkbox"]')
                                .forEach(checkbox => checkbox.disabled = true);

                            if (solution) {
                                solution.style.display = 'block';
                            }
                        }
                    } else {
                        const goodCheckboxes = ul.querySelectorAll('input.good');
                        goodCheckboxes.forEach(checkbox => {
                            checkbox.checked = true;
                        });

                        const solution = ul.parentElement.querySelector('.solution');

                        if (solution) {
                            solution.style.display = 'block';
                        }

                        ul.querySelectorAll('input[type="checkbox"]')
                            .forEach(checkbox => checkbox.disabled = true);

                        ul.parentElement.classList.add('fail');
                    }
                }
            });
        });
    });

    function findParentWithClass(element, className) {
        if (element.classList && element.classList.contains(className)) {
            return element;
        }
        if (element.parentElement == null) {
            return null;
        }
        return findParentWithClass(element.parentElement, className);
    }

    Array.from(document.querySelectorAll('.text-with-gap')).forEach(input => {
        input.addEventListener('input', () => {
            const answer = input.getAttribute('answer') || input.dataset.solution;
            if (input.value.trim().toLowerCase() === answer.toLowerCase()) {
                input.classList.add('good');
                input.classList.remove('bad');
            } else {
                //input.classList.add('bad');
                input.classList.remove('good');
            }

            // Get the input parent having .text-with-gap class
            const parent = findParentWithClass(input, 'fill-in-the-blank');
            // If all inputs have the class `good`, we associate class `pass` to the parent .admonition.exercise

        });
    });

    Array.from(document.querySelectorAll('.fill-in-the-blank')).forEach(exercise => {
        exercise.querySelector('.exercise-title').addEventListener('click', function(event) {
            // Reset the exercise
            exercise.classList.remove('pass');
            exercise.classList.remove('fail');
            exercise.querySelectorAll('input').forEach(input => {
                input.disabled = false;
                input.value = '';
                input.classList.remove('good');
                input.classList.remove('bad');
            });
            // Show the submit button (block n'est pas le bon display)
            exercise.querySelector('button.exercise-submit').style.display = 'inline';
            // Hide the solution
            const solution = exercise.querySelector('.solution');
            if (solution) {
                solution.style.display = 'none';
            }
            const hint = exercise.querySelector('.hint');
            if (hint) {
                hint.style.display = 'block';
            }
        });


        exercise.querySelector('button.exercise-submit').addEventListener('click', () => {
            const allInputs = exercise.querySelectorAll('input');
            const allGoodInputs = exercise.querySelectorAll('input.good');
            console.log(exercise, allInputs, allGoodInputs);
            if (allInputs.length === allGoodInputs.length) {
                exercise.classList.add('pass');
                exercise.classList.remove('fail');
            } else {
                exercise.classList.remove('pass');
                exercise.classList.add('fail');
            }

            // Disable all inputs
            allInputs.forEach(input => {
                if (input.classList.contains('good')) {
                    input.classList.add('good');
                    input.classList.remove('bad');
                } else {
                    input.classList.add('bad');
                    input.classList.remove('good');
                }
                input.disabled = true

                // Add answers to the inputs
                const answer = input.getAttribute('answer') || input.dataset.solution;
                input.value = answer;
            });

            // Show the solution and hide the submit button
            const solution = exercise.querySelector('.solution');
            if (solution) {
                solution.style.display = 'block';
            }
            const hint = exercise.querySelector('.hint');
            if (hint) {
                hint.style.display = 'none';
            }
            exercise.querySelector('button.exercise-submit').style.display = 'none';
        });
    });
});
