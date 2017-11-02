# 07-Breakout
                  __
                 /.-
         ______ //
        /______'/|
        [       ]|
        [ Grape ]|
        [ Juice ]|
        [  _\_  ]|
        [  :::  ]|
        [   :'  ]/
        '-------'

Adds these juicy features:
 -lots and lots of blocks to take down, 25 lives
 -Each block has a random color
 -Ball has a random color each time it is reset (will always be dark)
 -Background switches between a gradient of random colors
 -Background music (An instrumental cover of Jailbreak by Thin Lizzy)
 -Sound effects for breaking block, losing a ball, and hitting a ball
 -Game over screens for winning and losing (with music!)
 -Restart game by pressing a key
 -Particle effects when breaking a block

---------------------------------------------------------------------------------------------------------------------

PS:

This code:

    for x in range(0, len(p_list)):
        try:
            # check if the particle is no longer colliding with the screen
            if p_list[len(p_list) - x - 1].rect.y > screen_size[1]:
                # remove the particle from the list
                del p_list[len(p_list) - x - 1]

gets out of range because you take len(p_list) - len(p_list) - 1, which is -1. There is no p_list[-1].

---------------------------------------------------------------------------------------------------------------------

This is the sixth assignment for ILS-Z399: the classic game of breakout. Originally built by Steve Wozniak (and aided by Steve Jobs), this has been an arcade classic since 1976.

This version of breakout should be working, but it is pretty boring. Your assignment is to make it "juicy": use your creativity and the tools we have been talking about in class to make it more fun to play.

I have tried to leave you some hooks into which you can inject your code, but let me know if you run into trouble. Here are some resources that might help:

* [Juice it or lose it - a talk by Martin Jonasson & Petri Purho](https://www.youtube.com/watch?v=Fy0aCDmgnxg)
* [Easing Equations in Python (orig by Robert Penner)](https://gist.github.com/th0ma5w/9883420)
* [PyGame Tutorial: Working with Images](http://www.nerdparadise.com/programming/pygame/part2)
* [PyGame Tutorial: Music and Sound Effects](http://www.nerdparadise.com/programming/pygame/part3)
* [pygame shaking window when losing lives](https://stackoverflow.com/questions/23633339/pygame-shaking-window-when-loosing-lifes)
* [Some pygame examples for you to play with](https://github.com/ILS-Z399/pygame-examples)
* [Degrees and Radians](https://www.quia.com/jg/321176list.html)

To complete this assignment you will need to understand:

* Python Classes, objects, and other data structures
* The pygame game engine

---

The grading criteria will be as follows:

* [1 point] Assignment turned in on time
* [1] Repository contains an appropriate software license
* [2] Repository contains a descriptive README.md
* [1] Requires Python 3
* [1] No syntax errors
* [8] Accomplishes the objective of the assignment
* [2] No other runtime errors
* [2] Validates user input (if necessary)
* [2] Adds interesting features (beyond the scope of the assignment)

20 points total