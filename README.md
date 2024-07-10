# Mkdocs Exercise Plugin

This plugin is a simple exercise plugin for MkDocs. It allows you to add exercises to your markdown files and have them automatically checked when the page is loaded.

## Development

```bash
poetry install
pip install -e .
poetry run python serve.py
```

## User Experience

### Login

Login is only frontend. It can use a **Microsoft** login page to get the user's email. Since our institution uses Microsoft accounts, this is a good way to get the user's email.

Logged in users will stay logged in until they log out. The email is stored in the browser's local storage.

We could use some kind of cloud database to store the analytics data: who answered what, when, and how many times. This would allow us to track the student's progress and see how they are doing.

When a student logs in their exercises done are then restored.

### Exercises pages (Drill)

All exercises from the course are listed in the exercises page. The student can toggle some switches:

- Reset all exercises (this action is irreversible)
- Show only exercises that are not done
- Sort by tags, difficulty (for instance the student would exercise with pointers only, he will select the tag "pointers")

A summary can be displayed to show the student's progress. Pie charts can show how many exercises are done, how many are not done, and how many are correct and incorrect.

We could also add a search bar to search for exercises by name.

## Type of questions

1. Multiple choice questions
2. Fill in the blanks
3. Code exercises

## To do

- [ ] Add fill-in-the-gap in mermaid, can add an overlay in diagrams or any svg

## Notes

### Mermaid overlay

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVG with Input</title>
    <style>
        .container {
            position: relative;
            width: 300px; /* Set the width you want */
            height: 200px; /* Set the height you want */
        }
        svg {
            width: 100%;
            height: 100%;
        }
        .input-overlay {
            position: absolute;
            width: 100px; /* Set the width you want for the input */
        }
    </style>
</head>
<body>
    <div class="container">
        <svg id="svg-element" viewBox="0 0 300 200">
            <rect x="0" y="0" width="300" height="200" fill="lightgrey" />
            <text x="50" y="30" font-family="Arial" font-size="24">
                Your <tspan id="tspan-element">SVG</tspan> Content
            </text>
        </svg>
        <input class="input-overlay" type="text" placeholder="Type here" id="input-overlay" />
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const tspanElement = document.getElementById('tspan-element');
            const inputOverlay = document.getElementById('input-overlay');

            const svgElement = document.getElementById('svg-element');
            const svgRect = svgElement.getBoundingClientRect();
            const tspanRect = tspanElement.getBoundingClientRect();

            // Calculate the position relative to the container
            const top = tspanRect.top - svgRect.top;
            const left = tspanRect.left - svgRect.left;

            // Position the input element
            inputOverlay.style.top = `${top}px`;
            inputOverlay.style.left = `${left}px`;
        });
    </script>
</body>
</html>
```