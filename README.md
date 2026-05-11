# Mood Art Visualizer
## Demo
#### Video Demo: [https://youtu.be/6ZcWuuREmsU]
#### Github Repository: [https://github.com/selinarlin/mood-art-visualizer/tree/main#]
## Description
This **Mood Art Visualizer** is a python project that created animated particle art based on the user's chosen emotions. Once this program runs, the user will be met with a menu screen, where user can choose any of the four mood options. Once a mood is selected, it will transport the screen to a display of moving particles trails with the mood associated colors.

The four moods:
- Calm
- Mad
- Sad
- Nostalgic

Each mood has its own related background color, particle colors, and movement style. For example, mad has a energetic pallete of red and orange, moving at a fast pace, while sad uses darker colors like blue and purple, moving at a slower pace.

The particles move in a circular spiral motion round the screen. It slowly fades out, creating a smooth animated effect. Random values are used for colors, sizes, directions, and positions to ensure variety each time the program runs.

## Files and Classes
This project used mainly one python file

### `Particle` Class
The `Particle` class creates and controls the individual particles.
It controls:
- Particle movement
- Particle colors
- Particle lifespan
- Particle fading effect
- Drawing particle on screen

### `ParticleTrail` Class
The `ParticleTrail` class creates the spiral trails.
It controls:
- Spiral movement
- Particle spawns
- Spiral rotation speed
- random trail positions

### `App` Class
The `App` class controls the whole program:
- The menu screen
- Buttons
- Mood selection
- Main program loop
- Switching between screens

## Design Choices

An important part when creating this project was ensuring the uniqueness of each mood screen. Each colors and motion were carefully selected to match each mood accordingly, so users are able to connect emotionally with their choose visual. 

## Future Improvements

Some improvements that could be made later on include:
- More mood options
- Sound or music
- More particle effects
- More dramatic/ smoother spirals
- Option for user customization

## Technologies Used

- Python
- Pygame

## How to Run

1. Install Python
2. Install Pygame:
```bash
pip install pygame
```
3. Run the file
```bash
python project.py
```

## Author

Created by Selina Lin
