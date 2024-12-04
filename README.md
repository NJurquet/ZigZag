<h1 align="center">ZigZag</h1><br>
<div align="center">
<img src="https://play-lh.googleusercontent.com/6pyha8P40IH8Yn7ets-yr-sDmze-lif7Lh80ZMffdBojvhAtGTk88zHru3UHeipNhA" width="300" /><br>
</div>

## Depedencies
This project uses depedencies that require `Python 3.10` or above.
<div align="center">
  
| **Name** | **Version Used** |
|----------|:----------------:|
| Python   | 3.12.4           |
| OpenCV   | 4.10.0.84        |
| Numpy    | 2.1.3            |
| PyWin32  | 308              |
</div>


## Strategy
1. Detect the player ball and draw a circle with OpenCV.
2. Detect path edges and draw the lines with OpenCV.
3. Find optimal parameters & filter detected objects to keep the necessary ones.
4. If the ball is close enough to the corresponding edge, simulate a click.

## Difficulties

### Changing colors
As we progress through one game, the theme will randomly change color. It is also possible for the player to choose a ball skin/color.

Any color-based processing will therefore be quite limited.

### Precise detection
OpenCV might not find all edges or perfect lines. It is therefore a must to find a way to still be able to check if the ball is near the edge or not.

### Diamonds
Pink diamonds are not part of the game logic but are still isometric shapes made up from lines.
They will therefore interfere with lines detection and maybe cause unwanted change in ball direction.

### Real-time game
Objects detection, screen processing & actions must be done on a moving screen image with minimal lag.
Processing and computations must be fast to avoid impacting gameplay.

### Window capture
This program is meant to be efficient and reproducible. So, the game window position should be independent of the resulting performance of the program.

The game window capture must also not introduce disturbances or noise that can affect performance or gameplay.

### Computer independence
The program should work properly on every computer, whether it has good/bad performance, high/low resolution or runs on Windows/macOS.
