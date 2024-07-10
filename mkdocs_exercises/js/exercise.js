
console.log("Hello from exercise.js");

document.addEventListener("DOMContentLoaded", function () {

    Array.from(document.getElementsByClassName('exercise-list')).forEach(ul => {

        ul.addEventListener('change', function (event) {
            if (event.target && event.target.matches('input[type="checkbox"]')) {
                const isGood = event.target.classList.contains('good');
                if (isGood) {
                } else {
                    const goodCheckboxes = ul.querySelectorAll('input.good');
                    goodCheckboxes.forEach(checkbox => {
                        checkbox.checked = true;
                    });

                    const solution = ul.parentElement.querySelector('.solution');
                    // If element is not a tag <detail>


                    if (solution) {
                        solution.style.display = 'block';
                    }

                    ul.querySelectorAll('input[type="checkbox"]')
                        .forEach(checkbox => checkbox.disabled = true);
                }
            }
        });
    });


    const inputs = document.querySelectorAll('.text-with-gap');

    inputs.forEach(input => {
        input.addEventListener('input', () => {
            const answer = input.getAttribute('answer') || input.dataset.solution;
            if (input.value.trim().toLowerCase() === answer.toLowerCase()) {
                input.classList.add('good');
                input.classList.remove('bad');
            } else {
                input.classList.add('bad');
                input.classList.remove('good');
            }
        });
    });

});
