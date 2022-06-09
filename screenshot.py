import pyautogui

def screenshot(dirname):
    relator_path = dirname + "\\static\\relator_for_screenshot.jpg"

    location = pyautogui.locateOnScreen(relator_path, confidence=0.7)
    myScreenshot = pyautogui.screenshot(region=(location.left+1, location.top-400, location.width, location.height+360))

    screenshot_path = dirname + "\\static\\screenshots\\screenshot.jpg"
    #myScreenshot = pyautogui.screenshot(region=(100, 100, 500, 400))S
    myScreenshot.save(r"{}".format(screenshot_path))