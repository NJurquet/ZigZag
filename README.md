<h1 align="center">ZigZag</h1><br>
<div align="center">
<img src="https://play-lh.googleusercontent.com/6pyha8P40IH8Yn7ets-yr-sDmze-lif7Lh80ZMffdBojvhAtGTk88zHru3UHeipNhA" width="300" /><br>
</div>

## Introduction

### Game

**ZigZag** is a popular mobile game with over 50M downloads on the Google Play Store.
The game is simple: the player controls a ball that moves on an isometric zigzag path and changes direction when the player tap on the screen.
A direction change will therefore move the ball diagonally to the left or right.
The goal is to stay on the path as long as possible without falling off the edges and collect as much diamonds as possible.

Each tap/turn will increase the score by 1.
When picking up a diamond, the score will increase by 2.
These diamonds can then be used to unlock new ball skins.

The game has 5 Google Play Games achievements:

-   Get a score of 50 points! (Uncommon)
-   Get a score of 125 points! (Uncommon)
-   Get a score of 250 points! (Rare)
-   Get a score of 1000 points! (Ultra Rare)
-   Play 1000 rounds of ZigZag! (Rare)

### Project

This project aims to create a bot that will play the game for the player using `Python` image processing.
`OpenCV` & `Numpy` are used for every image processing task.
Considering it is a mobile game, an Android emulator (eg. Bluestacks, LDPlayer) must be used to run the game on a computer.

The bot detects the ball and path edges, then simulates a click when the ball is close to an edge.
This bot is implemented to get all the score achievements and the highest score possible.

> [!NOTE]
> The bot is only working on **Windows** at the moment, and has been tested on **Visual Studio Code** (even though it should work on any IDE) and **Bluestacks** Android emulator.

## Depedencies

This project uses depedencies that require `Python 3.10` or above.

<div align="center">
  
|    **Name**    | **Version Used** |
|----------------|:----------------:|
| Python         | 3.12.4           |
| opencv-python  | 4.10.0.84        |
| numpy          | 2.1.3            |
| pywin32        | 308              |
| PyAutoGUI      | 0.9.54           |
</div>

## Installation

> [!WARNING]
> **MacOS** is not supported at the moment.

1. Clone the repository and navigate to the project root folder `ZigZag`:

```bash
git clone https://github.com/NJurquet/ZigZag.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Install an Android emulator on your computer.
   [Bluestacks](https://www.bluestacks.com/) or [LDPlayer](https://www.ldplayer.net/) are recommended.

4. Go to the Google Play Store, sign in with your Google account and download **ZigZag**.

5. In the emulator settings, remove eventual ads.
   Minimize the right sidebar to remove a maximum of distractions.

6. Open the game and test a few games to make sure the game is running correctly (the emulator can be put in airplane mode for less ads, but it should not affect the bot).

7. Change the `src/config.py` file to configure the project as needed.

    Make sure to set the `WINDOW_NAME` constant to your game window name, and `VISION_EN` to `False` to disable the image processing window.
    A list of all opened windows can be obtained by running:

```bash
python -m src.capture.screen_capture
```

> [!TIP]
> Set `VISION_EN` to `False` to minimize the time used for frame drawing and display.

8. Make sure you have done the following before running the bot for the best results:

    - Have the game on the main screen
    - Your PC is charging (for better performance)
    - Any heavy other programs are closed (for better performance)

9. Run the bot:

```bash
python -m src.main
```

> [!NOTE]
> The window should automatically be resized to `WINDOW_HEIGHT` provided in the `config.py` file, and the mouse be moved to the center of the window.

## Goals

1. Process a frame image so it detects the ball and path edges.

2. Process the real-time game screen so it detects the ball and path edges.

3. Be able to simulate a click that results from the ball being close to an edge.

4. Have an average FPS of at least 30 with vision window enabled and when the PC is charging.

5. Achieve an average score of 500 points.

6. Achieve a score of 1000 points.

7. The game window should be captured no matter its initial position or size, and without causing more disturbances.

8. The bot should meet the 500 average points objective on any Windows computer, regardless of its performance or resolution.

9. The bot should be robust and give reproducible results. It should be independant to time, randomness, and other external factors.

## Strategy

1. Find the emulator window, resize it and move the mouse to its center.
2. Capture the window using DPI awareness for being able to capture DPI aware applications, and for screen scale independence.
3. Find optimal detection parameters & mask out interfering objects to keep the necessary ones.
4. Detect the player ball and draw a circle on the frame with OpenCV.
5. Detect path edges and draw the lines on the frame with OpenCV.
6. Use 2 points for edge proximity detection: horizontal front point & isometric front point. If the ball is close enough to a detected edge, it simulates a click.
7. When changing direction, vertically mirror the 2 points to only detect one side of the edges lines.
8. Also simulate a click when the white background is detected, in case edges are not detected properly.
9. All or most calculations are performed using matrix operations or Numpy arrays for processing time optimization.
10. Every position, distance or size are calculated in relative units to the screen height for window size & screen resolution independence.

## Difficulties

### Changing colors

As we progress through one game, the theme will randomly change color. It is also possible for the player to choose a ball skin/color.

Any color-based processing will therefore be very limited.

### Precise detection

OpenCV might not find all edges or perfect lines.
It is therefore a must to find a way to still be able to check if the ball is near the edge or not.

### Diamonds

Pink diamonds are not part of the game logic but are still isometric shapes made up from lines.
They will therefore interfere with lines detection and may cause unwanted change in ball direction.

### Real-time game

Objects detection, screen processing & actions are done on a real-time window image.
These operations takes time and if not optimized, will cause the bot to have a low reaction time, resulting in a delay in the ball direction change or in a failing edge detection.

### Window capture

The game window capture may also introduce disturbances or noise that can affect performance or gameplay.
If the window is not captured correctly, for example if the window has unexpected bars or borders, the bot will not be able to detect the ball/edges correctly.

The window will not be placed at the exact same position every time, so capturing the window based on its position will not work.

### Computer independence

The bot might run on computers with different/lower performance, and so every lag, glitch or processing time might take longer.
Computers also have different screen resolutions and scaling, so using fixed pixel sizes and positions will cause unexpected results or being out of the screen.
