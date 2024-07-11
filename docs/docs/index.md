# Demo Exercises

Here a few examples of exercises you can create with this plugin.

## Multiple choice questions

Adding the `multicolumn` keyword to the exercise block will allow displaying the choices in multiple columns.

The solution is only displayed when the exercise is validated.

```md
!!! exercise multicolumn "Deep Throught"

    What is the answer to the ultimate question of life, the universe,
    and everything?

    - [ ] 4
    - [ ] 8
    - [ ] 15
    - [ ] 16
    - [ ] 23
    - [x] 42

    !!! solution

        In the book "The Hitchhiker's Guide to the Galaxy" by Douglas Adams,
        the number 42 is the "Answer to the Ultimate Question of Life, the
        Universe, and Everything".

        This is a book you should read if you haven't already!
```

!!! exercise multicolumn "Deep Throught"

    What is the answer to the ultimate question of life, the universe, and everything?

    - [ ] 4
    - [ ] 8
    - [ ] 15
    - [ ] 16
    - [ ] 23
    - [x] 42

    !!! solution

        In the book "The Hitchhiker's Guide to the Galaxy" by Douglas Adams, the number 42 is the "Answer to the Ultimate Question of Life, the Universe, and Everything".

        This is a book you should read if you haven't already!

We could have a multiple choice question with multiple correct answers:

```md
!!! exercise "Duck"

    How many legs doesn't a duck have ?

    - [ ] 2
    - [x] 4
    - [x] 5

    !!! solution

        Ducks have 2 legs. The question was how many legs doesn't a
        duck have, so the answer is everything except 2.
```

!!! exercise "Duck"

    How many legs doesn't a duck have ?

    - [ ] 2
    - [x] 4
    - [x] 5

    !!! solution

        Ducks have 2 legs. The question was how many legs doesn't a duck have, so the answer is everything except 2.

## Fill in the blanks

Use the mustache syntax `{{...}}` to indicate the blanks:

```md
!!! exercise "Four Weddings and a Funeral"

    Fill in the blanks:

    1. Roses are {{red}},
    2. Violets are {{blue}},
    3. Sugar is {{sweet}},
    4. And so are you!

    ??? hint

        This is a classic poem.

    !!! solution

        This poem is a classic from the movie "Four Weddings and a Funeral".
        Andie MacDowell's character recites it to Hugh Grant's character.
```

!!! exercise "Four Weddings and a Funeral"

    Fill in the blanks:

    1. Roses are {{red}},
    2. Violets are {{blue}},
    3. Sugar is {{sweet}},
    4. And so are you!

    ??? hint

        This is a classic poem.

    !!! solution

        This poem is a classic from the movie "Four Weddings and a Funeral". Andie MacDowell's character recites it to Hugh Grant's character.

Here another example:

```md
!!! exercise "The Path"

    In the famous movie *Pulp Fiction* from Quentin Tarantino,
    Jules Winnfield recites a passage from the Bible before executing someone.

    Fill in the blanks:

    > The path of the righteous man is beset on all sides by the inequities
    of the {{selfish}} and the tyranny of evil men. Blessed is he who, in the
    name of charity and good will, shepherds the {{weak}} through the valley of
    darkness, for he is truly his brother's keeper and the {{finder}} of lost
    children. And I will strike down upon thee with great vengeance and furious
    anger those who attempt to poison and destroy my {{brothers}}. And you will
    know my name is the {{Lord}} when I lay my vengeance upon thee.
```

!!! exercise "The Path"

    In the famous movie *Pulp Fiction* from Quentin Tarantino, Jules Winnfield recites a passage from the Bible before executing someone.

    Fill in the blanks:

    > The path of the righteous man is beset on all sides by the inequities of the {{selfish}} and the tyranny of evil men. Blessed is he who, in the name of charity and good will, shepherds the {{weak}} through the valley of darkness, for he is truly his brother's keeper and the {{finder}} of lost children. And I will strike down upon thee with great vengeance and furious anger those who attempt to poison and destroy my {{brothers}}. And you will know my name is the {{Lord}} when I lay my vengeance upon thee.

You can also use regular expressions to match the blanks. The format is `/regex/preferred answer/flags`:

```md
!!! exercise "Satellite"

    Our planet is a satellite of the Sun. How many natural satellites does the
    Earth have?

    The Earth has {{/one|1/one/i}} natural satellite.
```

!!! exercise "Satellite"

    Our planet is a satellite of the Sun. How many natural satellites does the
    Earth have?

    The Earth has {{/one|1/one/i}} natural satellite.
