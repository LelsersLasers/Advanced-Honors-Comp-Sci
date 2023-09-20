import cv2
import argparse
import face_swap
import sys
import time
import pygame
import widgets

# ---------------------------------------------------------------------------- #
def setupPygame(fontPath):
    pygame.init()
    win = pygame.display.set_mode((700, 700), pygame.SRCALPHA)
    pygame.display.set_caption("Face Swap Pro Plus Platinum Edition Deluxe")
    
    font = pygame.font.Font(fontPath, 25)

    return win, font
# ---------------------------------------------------------------------------- #
def drawWindow(win, buttons, texts, rects):
    win.fill("#2E3440")
    for button in buttons:
        button.draw(win)
    for text in texts:
        text.draw(win)
    for rect in rects:
        rect.draw(win)
    
    pygame.display.flip()
# ---------------------------------------------------------------------------- #
def createWidgets(win, font):
    buttons = {
        "open": [],
        "run": [],
        "live": []
    }
    texts = {
        "open": [],
        "run": [],
        "live": []
    }
    rects = {
        "open": [],
        "run": [],
        "live": []
    }

    # create title screen
    text = widgets.Text(["center", "center"], "Face Swap Pro Plus Platinum Edition Deluxe", font, "nord6")
    text.centerX(0, 700)
    text.centerY(200, 700)
    texts["open"].append(text)

    image = widgets.Image([125, 50], 450, 450, "resources/TitleImage.jpg")
    rects["open"].append(image)

    # create menu screen
    text = widgets.Text(["center", 50], "Face Swap Pro Plus Platinum Edition Deluxe", font, "nord6")
    text.centerX(0, 700)
    texts["run"].append(text)

    rect = widgets.Rect([10, 125], 680, 6, "nord3", borderRadius=2)
    rects["run"].append(rect)

    text = widgets.Text(["center", 135], "Input Mode", font, "nord6")
    text.centerX(0, 700)
    texts["run"].append(text)

    others = []
    for i, inputType in enumerate(["Image", "Video", "Camera"]):
        x = 50
        y = 205
        w = 200
        text = widgets.Text([0, 0], inputType, font, "nord5")
        text.centerX(x + w * i, w)
        text.centerY(y, 50)
        rect = widgets.Rect([x + w * i + 1, y], 198, 50, "nord3", borderRadius=5)
        button = widgets.SingleSelectButton(text, rect, inputType, "white")
        others.append(button)

    for button in others:
        for other in others:
            if other is not button:
                button.others.append(other)
        buttons["run"].append(button)

    rect = widgets.Rect([10, 275], 680, 6, "nord4", borderRadius=2)
    rects["run"].append(rect)

    text = widgets.Text(["center", 290], "Path to Image", font, "nord6")
    text.centerX(0, 700)
    texts["run"].append(text)

    text = widgets.Text([0, 0], "Browse Files", font, "nord6")
    text.centerX(275, 150)
    text.centerY(360, 50)

    rect = widgets.Rect([275, 360], 150, 50, "nord4")
    button = widgets.FileBrowser(text, rect, "None", "red")
    buttons["run"].append(button)

    rect = widgets.Rect([10, 425], 680, 6, "nord4", borderRadius=2)
    rects["run"].append(rect)

    text = widgets.Text(["center", 440], "Save Output", font, "nord6")
    text.centerX(0, 700)
    texts["run"].append(text)

    rect = widgets.Rect([0, 500], 50, 50, "nord8", 5)
    text = widgets.Text([0, 500], "Save File:", font, "nord6")
    image = widgets.Image([0, 500], 45, 45, "resources/checkMark.png")

    checkMark = widgets.CheckMark(text, rect, False, image, 15, "save")
    checkMark.centerX(0, 700)
    buttons["run"].append(checkMark)

    text = widgets.Text([0, 560], "Filename:", font, "nord6")
    text.centerX(0, 700)
    textInput = widgets.TextInput([200, 610], 300, 75, "nord3", font, "nord6", "save_path")
    textInput.rerender()
    buttons["run"].append(textInput)

    rect = widgets.Rect([10, 700], 680, 6, "nord4", borderRadius=2)
    rects["run"].append(rect)

    text = widgets.Text([0, 710], "Continue", font, "nord6")
    rect = widgets.Rect([275, 710], 150, 60, "nord4", borderRadius=5)
    text.centerX(275, 150)
    text.centerY(710, 60)
    button = widgets.StateButton(text, rect, "live", "white")
    buttons["run"].append(button)

    # live value changes
    text = widgets.Text([0, 50], "Settings", font, "nord6")
    text.centerX(0, 700)
    texts["live"].append(text)

    rect = widgets.Rect([10, 125], 680, 6, "nord3", borderRadius=2)
    rects["live"].append(rect)

    text = widgets.Text([0, 150], "Confidence", font, "nord6")
    text.centerX(0, 700)
    texts["live"].append(text)

    slider = widgets.Slider([280, 200], 200, 75, "confidence", "confidence", font, minVal = 0, maxVal = 1, step = 0.1, color = "nord3", handleColor = "nord6", initial = 0.8, roundDig=2, circleHandle = False)
    buttons["live"].append(slider)

    rect = widgets.Rect([0, 300], 50, 50, "nord8", 5)
    text = widgets.Text([0, 300], "Blur:", font, "nord6")
    image = widgets.Image([0, 300], 45, 45, "resources/checkMark.png")

    checkMark = widgets.CheckMark(text, rect, False, image, 15, "blur")
    checkMark.centerX(0, 700)
    buttons["live"].append(checkMark)

    text = widgets.Text([0, 400], "Blur Thickness", font, "nord6")
    text.centerX(0, 700)
    texts["live"].append(text)

    slider = widgets.Slider([280, 450], 200, 75, "blur_thickness", "blur", font, minVal = 0, maxVal = 100, step = 1, color = "nord3", handleColor = "nord6", initial=40, circleHandle = False)
    buttons["live"].append(slider)

    text = widgets.Text([0, 550], "Blur Radius", font, "nord6")
    text.centerX(0, 700)
    texts["live"].append(text)

    slider = widgets.Slider([280, 600], 200, 75, "blur_radius", "blur", font, minVal = 0, maxVal = 100, step = 1, color = "nord3", handleColor = "nord6", initial = 15, circleHandle = False)
    buttons["live"].append(slider)

    buttons["live"][-3].setSetting(buttons["live"])

    rect = widgets.Rect([0, 700], 50, 50, "nord8", 5)
    text = widgets.Text([0, 700], "Oval:", font, "nord6")
    image = widgets.Image([0, 700], 45, 45, "resources/checkMark.png")

    checkMark = widgets.CheckMark(text, rect, False, image, 15, "oval")
    checkMark.centerX(0, 700)
    buttons["live"].append(checkMark)

    text = widgets.Text([0, 775], "Wait Time:", font, "nord6")
    text.centerX(0, 700)
    texts["live"].append(text)

    slider = widgets.Slider([280, 825], 200, 75, "wait_time", "wait-time", font, minVal = 0, maxVal = 1, step = 0.1, color = "nord3", handleColor = "nord6", initial = 0.4, roundDig=2, circleHandle = False)
    buttons["live"].append(slider)

    text = widgets.Text([0, 925], "Order Offset:", font, "nord6")
    text.centerX(0, 700)
    texts["live"].append(text)

    slider = widgets.Slider([280, 975], 200, 75, "order_offset", "order-offset", font, minVal = 0, maxVal = 10, step = 1, color = "nord3", handleColor = "nord6", initial = 1, circleHandle = False)
    buttons["live"].append(slider)

    rect = widgets.Rect([10, 1075], 680, 6, "nord4", borderRadius=2)
    rects["live"].append(rect)

    text = widgets.Text([0, 1085], "Stop", font, "nord6")
    rect = widgets.Rect([275, 1085], 150, 60, "nord4", borderRadius=5)
    text.centerX(275, 150)
    text.centerY(1085, 60)
    button = widgets.StateButton(text, rect, "run", "white")
    buttons["live"].append(button)

    return rects, texts, buttons
# ---------------------------------------------------------------------------- #
def getSingleSelectValue(buttons):
    for button in buttons:
        if isinstance(button, widgets.SingleSelectButton):
            if button.currentValue is not None:
                return button.currentValue.lower()
            else:
                return button.currentValue
        
def getFilePath(buttons):
    for button in buttons:
        if isinstance(button, widgets.FileBrowser):
            return button.filePath

def getSetting(buttons, state, setting):
    for button in buttons[state]:
        if button.setting == setting:
            if isinstance(button, widgets.SingleSelectButton):
                if button.currentValue is not None:
                   return button.currentValue.lower()
                else:
                    return button.currentValue
            elif isinstance(button, widgets.TextInput):
                if button.empty:
                    return None
                else:
                    return button.text
            else:
                return button.value
        else:
            ...
# ---------------------------------------------------------------------------- #
def getLiveArgs(args, buttons):
    for setting in ["confidence", "blur", "blur_thickness", "blur_radius", "oval", "wait_time", "order_offset"]:
        args[setting] = getSetting(buttons, "live", setting)

def getArgs(args, buttons):
    args["input"] = getSingleSelectValue(buttons["run"])
    args["path"] = getFilePath(buttons["run"])
    save = getSetting(buttons, "run", "save")
    if not save:
        args["save"] = None
    else:
        args["save"] = f"saves/{getSetting(buttons, 'run', 'save_path')}"
    getLiveArgs(args, buttons)
# ---------------------------------------------------------------------------- #
def main():
    # create objs for app
    win, font = setupPygame("resources/AnnieUseYourTelescope-Regular.ttf")
    rects, texts, buttons = createWidgets(win, font)

    run = True

    # Mouse button double click
    downL = False

    # which list to draw and interact with
    state = "open"

    # button selects
    textSelected = False

    # threading for openCv
    thread = None
    args = {
        "input": None,
        "path": None,
        "filename": None,
        "save": None,
        "confidence": None,
        "debug": False,
        "blur": None,
        "blur_thickness": None,
        "blur_radius": None,
        "oval": None,
        "wait_time": None,
        "order_offset": None,
        "quit": False
    }

    # for graphics and scrolling
    winSize = win.get_size()

    # for title screen
    openCounter = 0
    openThreshold = 6
    firstFrame = True

    # to make sure it is the same on all computers
    currentTime = time.time()
    delta = time.time()
    while run:
        mouse = pygame.mouse.get_pos()
        if not state == "open":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not downL:
                    downL = True

                    for button in buttons[state]:
                        if button.collide(widgets.DrawTemplate(mouse, 1, 1)) and button.possible:
                            if isinstance(button, widgets.SingleSelectButton):
                                button.setOthers()
                                for button in buttons[state]:
                                    if isinstance(button, widgets.FileBrowser):
                                        button.setCurrentType(getSingleSelectValue(buttons[state]))
                            elif isinstance(button, widgets.FileBrowser):
                                button.setCurrentType(getSingleSelectValue(buttons[state]))
                                button.browseFiles()
                            elif isinstance(button, widgets.CheckMark):
                                button.flipValue()
                                button.setSetting(buttons[state])
                            elif isinstance(button, widgets.TextInput):
                                button.setSelected(True)
                                if button.selected:
                                    textSelected = True
                            elif isinstance(button, widgets.StateButton):
                                if state == "live" and button.value == "run":
                                    args["quit"] = True
                                    state = button.value
                                    continue
                                else:
                                    if button.checkConditions(buttons["run"]):
                                        if button.value == "live":
                                            getArgs(args, buttons)
                                            args["quit"] = False
                                        thread = button.changeState(args)
                                        if thread is not None:
                                            state = button.value

                            elif isinstance(button, widgets.Slider):
                                button.selected = not button.selected
                            
                            break
                        if isinstance(button, widgets.TextInput):
                            button.setSelected(False)
                            textSelected = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    downL = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and textSelected:
                        for button in buttons[state]:
                            if isinstance(button, widgets.TextInput) and button.selected and button.save:
                                button.setSelected(False)
                        textSelected = False
                    else:
                        for button in buttons[state]:
                            if isinstance(button, widgets.TextInput) and button.selected and button.save:
                                if event.key == pygame.K_BACKSPACE:
                                    button.text = button.text[:-1]
                                    if button.text == "":
                                        button.empty = True
                                else:
                                    button.text += event.unicode
                                    button.empty = False
                                button.rerender()
                
                elif event.type == pygame.MOUSEWHEEL:
                    y = event.y * 2
                    if event.flipped:
                        y *= -1
                    
                    if (y < 0 and buttons[state][-1].pt[1] + buttons[state][-1].h + 25 > winSize[1]) or (y > 0 and texts[state][0].pt[1] < 25):
                        for button in buttons[state]:
                            button.move(y)
                        for rect in rects[state]:
                            rect.pt[1] += y
                        for text in texts[state]:
                            text.pt[1] += y 
            
            if state == "live":
                if args["quit"]:
                    state = "run"
                    args["quit"] = False
            
            hover = False
            for item in buttons[state]:
                if hover:
                    item.setHover(False)
                elif item.collide(widgets.DrawTemplate(mouse, 1, 1)):
                    hover = True
                    item.setHover(True)
                else:
                    item.setHover(False)
            if state == "live":
                getLiveArgs(args, buttons)
        else:
            delta = time.time() - currentTime
            currentTime = time.time()
            if firstFrame:
                firstFrame = False
            else:
                openCounter += delta
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type in [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL]:
                    state = "run"
            
            time.sleep(0.01)

            if openCounter >= openThreshold:
                state = "run"

        drawWindow(win, buttons[state], texts[state], rects[state])


main()
