from ctypes import windll
import numpy as np
import win32api
import win32con
import win32gui
import win32ui

from config import Align


class ScreenCapture:
    user32 = windll.user32

    @staticmethod
    def capture_window(window_name: str) -> np.ndarray:
        """
        Captures the window with the specified name and returns an usable numpy array of the image.

        Parameters
        ----------
        `window_name` : `str`
            The name of the window to capture.

        Returns
        -------
        `np.ndarray`
            The captured window as a continguous numpy array.

        Raises
        ------
        `ValueError`
            If the window with the specified name is not found.
        """
        # Make the program DPI aware to prevent scaling issues & capture
        # hardware accelerated windows (e.g. Chrome, Windows Calculator)
        # https://stackoverflow.com/questions/76373625/pywin32-cannot-capture-certain-windows-giving-black-screen-python-windows
        ScreenCapture.user32.SetProcessDPIAware()

        hwnd = ScreenCapture.find_window(window_name)

        # Get window dimensions
        left, top, right, bottom, width, height = ScreenCapture._get_window_dimensions(hwnd)
        # Get the window's title bar height, in pixels.
        title_bar_height = win32api.GetSystemMetrics(win32con.SM_CYMENUCHECK) * 2
        window_border_w = win32api.GetSystemMetrics(win32con.SM_CYFRAME)

        # Get window device context
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        dc_obj = win32ui.CreateDCFromHandle(hwnd_dc)
        comp_dc = dc_obj.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(dc_obj, width, height)
        comp_dc.SelectObject(bitmap)

        # Captures the window image
        # If Special K is running, this number is 3. If not, 1
        result = ScreenCapture.user32.PrintWindow(hwnd, comp_dc.GetSafeHdc(), 3)

        # Convert window to numpy array
        bmp_str = bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmp_str, dtype=np.uint8).reshape((height, width, 4))

        # Make image C_CONTIGUOUS & drop the Alpha channel
        img = np.ascontiguousarray(img[..., :3])

        # Crop the title bar from the image
        img = img[title_bar_height+window_border_w:height-window_border_w, window_border_w:width-window_border_w]

        # Free resources
        dc_obj.DeleteDC()
        comp_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        win32gui.DeleteObject(bitmap.GetHandle())

        return img

    @staticmethod
    def find_window(window_name: str) -> int:
        """
        Finds the window with the specified name and returns its handle.

        Parameters
        ----------
        `window_name` : `str`
            The name of the window to find.

        Returns
        -------
        `int`
            The handle of the window.

        Raises
        ------
        `ValueError`
            If the window with the specified name is not found.
        """
        hwnd = win32gui.FindWindow(None, window_name)
        if not hwnd:
            raise ValueError(f"Window '{window_name}' not found")
        return hwnd

    @staticmethod
    def _get_window_dimensions(hwnd: int) -> tuple[int, int, int, int, int, int]:
        """
        Gets the dimensions of the window with the specified handle.

        Parameters
        ----------
        `hwnd` : `int`
            The handle of the window.

        Returns
        -------
        `tuple[int, int, int, int, int, int]`
            The dimensions of the window in the order: left, top, right, bottom, width, height.
        """
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        return left, top, right, bottom, width, height

    @staticmethod
    def set_window_pos_size(window_name: str, target_height: int, align: Align = Align.NONE) -> None:
        """
        Sets the window with the specified name to the specified height and aligns it accordingly.

        Parameters
        ----------
        `window_name` : `str`
            The name of the window to set the size of.
        `target_height` : `int`
            The target height of the window in pixels.
        `align` : `Align`, optional
            Window alignment relative to the screen. If set to `Align.NONE`, the window will keep its current position, by default `Align.NONE`

        Raises
        ------
        ValueError
            If the specified alignment is invalid.
        """
        ScreenCapture.user32.SetProcessDPIAware()
        hwnd = ScreenCapture.user32.FindWindowW(None, window_name)
        # hwnd = win32gui.FindWindow(None, window_name)

        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        # Restore the window if it is minimized or maximized
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

        # win32gui.BringWindowToTop(hwnd)
        win32gui.SetActiveWindow(hwnd)
        win32gui.SetForegroundWindow(hwnd)

        left, top, right, bottom, width, height = ScreenCapture._get_window_dimensions(hwnd)
        a_ratio = width / height
        target_width = round(target_height * a_ratio)

        if align == Align.LEFT:
            x, y = 0, 0
        elif align == Align.CENTER:
            screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            x = (screen_width - target_width) // 2
            y = (screen_height - target_height) // 2
        elif align == Align.RIGHT:
            screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            x = screen_width - target_width
            y = 0
        elif align == Align.NONE:
            x, y = left, top
        else:
            raise ValueError(f"Invalid alignment: {align} (expected: Align.LEFT, Align.CENTER, Align.RIGHT, Align.NONE)")

        # win32gui.MoveWindow(hwnd, x, y, target_width, target_height, True)
        ScreenCapture.user32.SetWindowPos(hwnd, None, x, y, target_width, target_height,
                                          win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE | win32con.SWP_SHOWWINDOW | win32con.SWP_FRAMECHANGED)

    @staticmethod
    def list_window_names():
        """
        Prints all open window names and handles.
        """
        # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)


if __name__ == "__main__":
    ScreenCapture.list_window_names()
