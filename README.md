# PCBS: Role of learning in three dimensional form perception
---

This project aims at reproducing part of the experiment conducted by Pawan Sinha and Tomaso Poggio in 1996, that was described in the article [Role of learning in three dimensional form perception](https://www.nature.com/articles/384460a0).

## Description of the original experiment

### The role of learning in shape perception
In the original experiment, Sinha and Poggio studied the role of learning in shape perception. To do so, they created several 3D shapes by randomly bending a 3D wire. This shape was rotating around an axis, and participants could see it projected on the screen. After seeing the projection, they had to say whether or not the shape seemed rigid. Two sets of shapes (A and B) were created, and the participants were randomly assignated to one of three groups:
+ Group 1: The participants underwent a training session with the set of images A, then a testing session with the set of images B.
+ Group 2: The participants only had a testing session with either the set of images A or the set of images B.
+ Group 3: The participants underwent a training session with the set of images B, then a testing session with the set of images A.

Sinha and Poggio showed that the participants reported non-rigidity more often during the training session than during the testing session, which suggests that the visual experience shapes the perception of 3D-form.

### Illusion: the walking man
This illusion is cited as an example by Sinha and Poggio: by creating a shape and making it rotate accordingly, one can have the feeling that it is a man walking in 2D rather than a 3D shape rotating.

## Overview of the computation

In order to project 3D shapes on a 2D plane, one first defines this plane through its normal vector, which is characterized by two angles alpha and beta:
