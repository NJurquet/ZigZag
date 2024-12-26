import pyautogui


class Actions:
    @staticmethod
    def click(x: int | None = None, y: int | None = None) -> None:
        """
        Simulates a mouse click at the specified coordinates. By default, it clicks at the current mouse position.

        Parameters
        ----------
        `x` : `int`, optional
            The x-coordinate of the click, by default `None`
        `y` : `int`, optional
            The y-coordinate of the click, by default `None`
        """
        pyautogui.click(x, y)

    @staticmethod
    def move_to(x: int, y: int) -> None:
        """
        Moves the mouse to the specified coordinates.

        Parameters
        ----------
        `x` : `int`
            The x-coordinate of the mouse.
        `y` : `int`
            The y-coordinate of the mouse.
        """
        pyautogui.moveTo(x, y)

    @staticmethod
    def press_key(key: str) -> None:
        """
        Simulates a key press.

        Parameters
        ----------
        `key` : `str`
            The key to press.
        """
        pyautogui.press(key)
