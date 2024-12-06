from ctypes import windll
import numpy as np
import win32gui
import win32ui


class ScreenCapture:
    @staticmethod
    def capture_window(window_name: str) -> np.ndarray:
        # Make the program DPI aware to prevent scaling issues & capture
        # hardware accelerated windows (e.g. Chrome, Windows Calculator)
        # https://stackoverflow.com/questions/76373625/pywin32-cannot-capture-certain-windows-giving-black-screen-python-windows
        windll.user32.SetProcessDPIAware()

        hwnd = win32gui.FindWindow(None, window_name)
        # hwnd = win32gui.GetDesktopWindow()
        if not hwnd:
            raise Exception(f"Window '{window_name}' not found")

        # Get window dimensions
        # Equivalent to "win32gui.GetWindowRect(hwnd)" for DPI
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        width = right - left
        height = bottom - top

        # Get window device context
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        dc_obj = win32ui.CreateDCFromHandle(hwnd_dc)
        comp_dc = dc_obj.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(dc_obj, width, height)
        comp_dc.SelectObject(bitmap)

        # Captures the window image
        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(hwnd, comp_dc.GetSafeHdc(), 3)

        # Convert window to numpy array
        bmp_str = bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmp_str, dtype=np.uint8).reshape((height, width, 4))

        # Make image C_CONTIGUOUS & drop the Alpha channel
        img = np.ascontiguousarray(img[..., :3])

        # Free resources
        dc_obj.DeleteDC()
        comp_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        win32gui.DeleteObject(bitmap.GetHandle())

        return img

    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)


if __name__ == "__main__":
    ScreenCapture.list_window_names()
