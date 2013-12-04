# Pickey

Pickey is an optimized keyboard layout generator. This web application collects user typing data and uses these metrics as fitness constraints in a genetic algorithm to find a better, personalized alternative to the QWERTY board.  Layouts are optimized for speed, learning curve, bigram frequency, and typing comfort.   In addition to keyboard generation, users can add and test boards created by other users, and visually edit their existing ones.  This application was constructed with D3, Python, Javascript, Flask, Jinja, and SQLalchemy.

## Typing Data Collection
### templates/keyboard.html, templates/input2.html

    Typing data is collected in two phases: a response to an open-ended prompt and the re-typing of a given text sample. The web app accepts minimal input, but greater amounts lead to better metrics and layout generation.  Users may click the "Repeat" button present in both phases to generate a new prompt and allow for additional input.

    Data is collected in the browser using Javascript/jQuery and is triggered by any keydown or keyup events. The event type, keycode, and timestamp is recorded for each keystroke and input sequence is also preserved to keep data about shifted values and bigrams usage.

    The visual keyboard in the browser uses keypress event listeners to animated the typing process.    

## Data Visualization
### templates/tests.html, genData.py, views.py

    A wide array of analytics can be derived from the simple act of typing. The dataset is processed in genData.py, and a fraction of it is binded to graphs. All of the data visualizations are created using D3.

    Analytics include: 
        Word per minute
        Typing accuracy
        Typing distance: Total distance, in mm, traveled by fingers when typing
        Finger percentages: Percentage of total typing completed by each finger 
        Hand usage percentages: Percentage of total typing completed by each hand 
        Letter frequencies: How often each letter was typed (light gray:least frequently, gray:frequently, blue:most frequently)
        Mistakes: Top three mistyped letters
        Dwell times: Time from keydown to keyup 
        Flight times: Time from one keydown to next keydown (dwell and flight times can be used in unique biometric profiling)
        Bigram times: Fastest and slowest bigram (two consecutive keys pressed) times from one keydown to next keyup
        Fastest bigram attributes: Most frequent finger, hand, movement characteristics from fastest bigram pairs
        Overall finger alteration: Percentages of same finger use and finger alteration to type bigrams
        Overall hand alteration: Percentages of same hand use and hand alteration to type bigrams
        Overall direction movement: Percentage of horizontal, vertical, and mixed movements to type bigrams

## Layout Generation
### templates/pekl.html, genData.py, genetic2.py

    With 51 interchangable keys, it is nearly impossibly to evaluated 51! layouts in a reasonable amount of time. Similarly, it is difficult to construct a single "best" layout with one attempt when the subject nature of the problem leads to the existance of multiple "good" layouts, which fulfil the constraints to some degree. To optimize the layout and compromise between all the constraints, Pickey uses a genetic algorithm to generate a pool of random layouts and mutate copies of the best participants. Keyboards are given a fitness score based upon three constraints: speed, comfort, and learning. Speed - distance of most frequent keys from homerow. Comfort - evaluating for hand, finger, and directional attributes of fastest bigrams. Learning - distance of keys from original qwerty layout. Keyboards that persist for multiple rounds are placed in an optimized pool, which is evaluated at the end for the final layout.

    The genetic algorithm takes time to complete and uses an ajax call upon page load.  

    Keys locations are remapped within the database and then rendered accordingly in the browser.

## Visual Keyboard Editor
### templates/edit.html

    The visual keyboard editor is available in the user's home page by clicking on the circular pen icon in the lower right corner of the keyboard image. The editor uses jQuery's Draggable and Droppable UI to move and resize the keys. Location changes are saved to the database using an AJAX call. As a default, the keyboard is assigned a randomly generated name, which may be changed in the editing mode, using another AJAX call.

## MISC
    
    Add: Keyboard layouts from other users may be found in the search tab and added to the user's inventory.
    Delete: Layouts that the user owns may be deleted in the home tab by clicking on the X in the upper-right corner of the keyboard image
    Typing: Layout keyboard is rendered in the browser and the user can practicing typing.
    Testing: User accuracy and wpm for new layouts can be tracked overtime to see improvement and the previous creation analytics


