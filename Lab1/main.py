import cv2
import argparse
import face_swap
import sys
import time
import pygame
import widgets

# ---------------------------------------------------------------------------- #
def setupPygame(fontPath) -> pygame.Surface:
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
        "image": []
    }
    texts = {
        "open": [],
        "run": [],
        "image": []
    }
    rects = {
        "open": [],
        "run": [],
        "image": []
    }

    # create title screen
    text = widgets.Text(["center", "center"], "Face Swap Pro Plus Platinum Edition Deluxe", font, "nord6")
    text.centerX(0, 700)
    text.centerY(0, 700)
    texts["open"].append(text)

    # create menu screen
    text = widgets.Text(["center", 25], "Face Swap Pro Plus Platinum Edition Deluxe", font, "nord6")
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
    image = widgets.Image([0, 500], 45, 45, "checkMark.png")

    checkMark = widgets.CheckMark(text, rect, False, image, 15)
    checkMark.centerX(0, 700)
    buttons["run"].append(checkMark)

    text = widgets.Text([0, 560], "Filename:", font, "nord6")
    text.centerX(0, 700)
    textInput = widgets.TextInput([200, 610], 300, 75, "nord3", font, "nord6")
    textInput.rerender()
    buttons["run"].append(textInput)

    rect = widgets.Rect([10, 700], 680, 6, "nord4", borderRadius=2)
    rects["run"].append(rect)

    text = widgets.Text([0, 710], "Continue", font, "nord6")
    rect = widgets.Rect([275, 710], 150, 60, "nord4", borderRadius=5)
    text.centerX(275, 150)
    text.centerY(710, 60)
    button = widgets.StateButton(text, rect, "image", "white")
    buttons["run"].append(button)

    return rects, texts, buttons
# ---------------------------------------------------------------------------- #
def getSingleSelectValue(buttons):
    for button in buttons:
        if isinstance(button, widgets.SingleSelectButton):
            return button.currentValue
# ---------------------------------------------------------------------------- #
def main():
    win, font = setupPygame("AnnieUseYourTelescope-Regular.ttf")
    rects, texts, buttons = createWidgets(win, font)

    run = True
    downL = False
    state = "open"
    textSelected = False
    winSize = win.get_size()
    openCounter = 0
    openThreshold = 2
    firstFrame = True
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
                        if button.collide(widgets.DrawTemplate(mouse, 1, 1)):
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
                                for bttn in buttons[state]:
                                    if isinstance(bttn, widgets.TextInput):
                                        bttn.setSave(button.value)
                            elif isinstance(button, widgets.TextInput):
                                button.setSelected(True)
                                if button.selected:
                                    textSelected = True
                            
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
                    y = event.y
                    if event.flipped:
                        y *= -1
                    
                    if (y < 0 and buttons[state][-1].pt[1] + buttons[state][-1].h + 25 > winSize[1]) or (y > 0 and texts[state][0].pt[1] < 25):
                        for button in buttons[state]:
                            button.pt[1] += y
                            if not isinstance(button, widgets.TextInput):
                                button.text.pt[1] += y
                            elif isinstance(button, widgets.CheckMark):
                                button.image.pt[1] += y
                        for rect in rects[state]:
                            rect.pt[1] += y
                        for text in texts[state]:
                            text.pt[1] += y 
            
            hover = False
            for item in buttons[state]:
                if hover:
                    item.setHover(False)
                elif item.collide(widgets.DrawTemplate(mouse, 1, 1)):
                    hover = True
                    item.setHover(True)
                else:
                    item.setHover(False)
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
            
            time.sleep(0.01)

            print(openCounter, delta, firstFrame)
            if openCounter >= openThreshold:
                state = "run"

        drawWindow(win, buttons[state], texts[state], rects[state])


main()
