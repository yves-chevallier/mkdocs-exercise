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

### Other Extensions

#### AllNumbering

MkDocs isn't quite ready for numbering elements such as:

- Sections / Headings
- Figures (`fig`)
- Tables (`tbl`)
- Codes (`code`)
- Admonitions / custom admonitions (`note`, `warning`, `tip`, `important`, `caution`, `danger`, `error`)
- Math equations (`eq`)

I see different numbering strategies:

1. Unique numbering for each type of element from 1 to N. All equations in all pages would be numbered from 1 to N, all figures from 1 to N, etc.
2. If section heading is enabled, then the numbers can be hierarchical. For instance, on section 2.2.3 the first equation would be numbered 2.1 and the second equation in the same section would be numbered 2.2. The number takes the chapter number and the element number.

Refs can be made to elements such as

```md
See figure @fig:myfigure.

![figure](figure.png){#fig:myfigure}
```

There are already some work on this:

- https://git.sr.ht/~ferruck/yafg which is obsolete
- https://github.com/flywire/caption which wasn't updated during the last year
- https://github.com/timvink/mkdocs-enumerate-headings-plugin which is only for headings

```yml
plugins:
  - allnumbering:
      enabled: true
      toc-depth: 0 # Up to which level the table of contents should be enumerated
      strict: true # Raise error if the numbering is not correct
      increment_across_pages: true # If the numbering should be incremented across pages
      restart_increment_after:
        - second_section.md

      equations:
        enabled: true
        style: [(arabic), roman, alphabetic] # 1.2.3, i.ii.iii, A.B.C
        # 0 Follow section headings from section level 0 (1.N)
        # 1 Follow section headings from section level 1 (1.2.N)
        # ...
        # false: flat numbering (default)
        hierarchical-depth: 0
      figures: true
      tables: true
      codes: true
      admonitions:
        types: [exercises] # List of custom admonitions that need numbering
      headings:
        style: arabic
        depth: 0 # Up to which level the headings should be enumerated
```

How to handle it in Markdown?

````md
# My section {#sec:mysection}

![caption](image.png){ #fig:myfigure }

![caption]() { #tbl:mytable }

| A | B | C |
|---|---|---|
| 1 | 2 | 3 |

```c { #code:myequation }
int main() { printf("Hello World!\n"); }
````

!!! note "My note" { #note:myadmonition }
    This is a note.

Table of figures / content / equations

```md
# Table of figures

{{{ listoffigures }}}
```

For this exercise plugin, then no need to number the exercises, the all-numbering plugin will take care of it.

The plugin could have two steps. First, altering the markdown with numbers, to be able to get output from pandoc for later processing. Second, take care of the presentation of the numbers in the html output.

#### Multicolumns

It would be nice to allow certain elements to be multicolumns, such as long lists. This would be an extension to the `pymdownx.blocks`

```markdown
{{{ multicolumn | 2

- [ ] 1
- [ ] 2
- [ ] 3
- [ ] 4

}}}
```

#### LaTeX directives

When exporting in LaTeX, it can be useful to have some directives to change the layout of the document. For instance, we could have a directive to change the layout to two columns.

```markdown
{{{ latex | \begin{multicols}{2}
- [ ] {{{ latex | \bfseries }}}1
- [ ] 2
}}}
```

#### Export to LaTeX ?

There is no plugin or extension to export to LaTeX. This could be useful for scientific papers or books. The plugin could be used to generate the LaTeX code and then the user could compile it with `pdflatex`.

There is already a plugin to export to PDF:

- https://github.com/alexandre-perrin/mkdocs-pandoc-plugin (3 years ago)
- https://github.com/HaoLiuHust/mkdocs-mk2pdf-plugin (5 years ago)

The goal is to simply parse Markdown using pandoc to LaTeX and support the custom extensions. This plugin should support additional LaTeX directives.

```md
@@ latex | \begin{multicols}{2}
@@ \end{multicols}

or inline

@@ latex | \textbf{ @@foobar@@ latex | } @@

or

@@ \frontmatter @@
```
