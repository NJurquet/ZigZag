# AI Project Usage

This document contains the prompts given to a particular AI and their corresponding responses.

## Prompts and Responses

For clarity, some part of the response code may be omitted and replaced with `...` if it's not relevant to the prompt or if the code has not changed.

### Window relative cropping

**Prompt:**

```
The game window has a title border at the top.
Update the `capture_window` method so this border is cropped from the image using the relative dimension of the window.
Also make sure it still works with win32 package and DPI awareness.
```

**Response:**

```py
import win32api
import win32con

class ScreenCapture:
    @staticmethod
    def capture_window(window_name: str) -> np.ndarray:

        ...

        # Get window dimensions
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        width = right - left
        height = bottom - top

        # Get the window's title bar height
        title_bar_height = win32api.GetSystemMetrics(win32con.SM_CYCAPTION)

        ...

        # Crop the title bar from the image
        img = img[title_bar_height:, :, :]
```

### Prompt 2

**Prompt:**

```
<Insert your prompt here>
```

**Response:**

```
<Insert AI response here>
```
