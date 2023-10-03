"""
    Description: Various graphical widgets for the supplementary Pygame GUI 
    Author: Millan and Jerry
    Date: 9/27/2023
"""

# Please just trust it works (we think)


from typing import Any
import pygame
import tkinter
from tkinter import filedialog
import os
import cv2
import face_swap

from thread_open_cv import CustomThread
# ---------------------------------------------------------------------------- #
colors = {
    "nord1": "#2E3440",
    "nord2": "#3B4252",
    "nord3": "#434C5E",
    "nord4": "#4C566A",
    "nord5": "#D8DEE9",
    "nord6": "#E5E9F0",
    "nord7": "#ECEFF4",
    "nord8": "#8FBCBB",
    "nord9": "#88C0D0",
    "nord10": "#81A1C1",
    "nord11": "#5E81AC",
    "nord12": "#BF616A",
    "nord13": "#D08770",
    "nord14": "#EBCB8B",
    "nord15": "#A3BE8C",
    "nord16": "#B48EAD",
    "transparent": (
        0,
        0,
        0,
        127
    )
}
# ---------------------------------------------------------------------------- #
class HoverEffect:
    def __init__(self, color, width):
        self.color = colors[color]
        self.width = width
    
    def draw(self, win, rect):
        pygame.draw.rect(win, self.color, pygame.Rect(rect.pt[0], rect.pt[1], rect.w, self.width))
        pygame.draw.rect(win, self.color, pygame.Rect(rect.pt[0] + rect.w, rect.pt[1], self.width, rect.h))
        pygame.draw.rect(win, self.color, pygame.Rect(rect.pt[0], rect.pt[1] + rect.h - self.width, rect.w, self.width))
        pygame.draw.rect(win, self.color, pygame.Rect(rect.pt[0], rect.pt[1], self.width, rect.h))
# ---------------------------------------------------------------------------- #
hoverEffects = {
    "white": HoverEffect("nord7", 2),
    "dark": HoverEffect("nord1", 2),
    "red": HoverEffect("nord12", 2)
}
# ---------------------------------------------------------------------------- #
class DrawTemplate:
    def __init__(self, pt: tuple[int, int], w: int, h: int):
        self.pt = pt
        self.w = w
        self.h = h

class Text:
    def __init__(self, pt, text, font, color):
        self.pt = pt
        self.text = text
        self.font = font
        self.color = colors[color]
        self.text_render = self.font.render(text, True, self.color)
    
    def get_width(self):
        return self.text_render.get_width()

    def get_height(self):
        return self.text_render.get_width()
    
    def centerX(self, x, w):
        self.pt[0] = x + w / 2 - self.text_render.get_width() / 2
    
    def centerY(self, y, h):
        self.pt[1] = y + h / 2 - self.text_render.get_height() / 2
    
    def draw(self, win):
        win.blit(self.text_render, self.pt)
    
    def render(self, text):
        self.text = text
        render = self.font.render(text, True, self.color)
        self.w = render.get_width()
        self.h = render.get_height()
        return render

    def rerender(self):
        self.text_render = self.render(self.text)
        
    
class Rect(DrawTemplate):
    def __init__(self, pt, w, h, color, width: int = 0, borderRadius: int = 0):
        super().__init__(pt, w, h)
        self.color = colors[color]
        self.width = width
        self.borderRadius = borderRadius
    
    def getRect(self):
        return pygame.Rect(self.pt[0], self.pt[1], self.w, self.h)
    
    def draw(self, win):
        if self.color is not None:
            pygame.draw.rect(win, self.color, self.getRect(), self.width, self.borderRadius)

class Circle(DrawTemplate):
    def __init__(self, pt: tuple[int, int], radius: int, color: str, width: int = 0):
        super().__init__(pt, radius, radius, width)
        self.color = color

    def draw(self, win):
        if self.color is not None:
            pygame.draw.circle(win, self.color, self.pt, self.w, self.width)

class Image(DrawTemplate):
    def __init__(self, pt, w, h, path):
        super().__init__(pt, w, h)
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, [w, h])
        self.path = path
    
    def draw(self, win):
        if self.image is not None:
            win.blit(self.image, self.pt)
    
class Button(DrawTemplate):
    def __init__(self, text: Text, rect: Rect, value, hoverEffect: str | None = None, setting: str | None = None):
        super().__init__(rect.pt, rect.w, rect.h)
        self.text = text
        self.rect = rect
        self.value = value
        self.hoverEffect = hoverEffect
        self.hover = False
        self.setting = setting
        self.possible = True
        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.surface.fill(colors["transparent"])
    
    def getSurface(self) -> pygame.Surface:
        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.surface.fill(colors["transparent"])

    def draw(self, win):
        self.rect.draw(win)
        self.text.draw(win)
        if self.hover and self.hoverEffect is not None:
            hoverEffects[self.hoverEffect].draw(win, self.rect)
        
        if not self.possible:
            win.blit(self.surface, self.pt)
    
    def collide(self, hb):
        return (
			self.pt[0] < hb.pt[0] + hb.w
			and hb.pt[0] < self.pt[0] + self.w
			and self.pt[1] < hb.pt[1] + hb.h
			and hb.pt[1] < self.pt[1] + self.h
		)
    
    def setHover(self, hover):
        self.hover = hover
    
    def setPossible(self, possible):
        if not possible == self.possible:
            self.possible = possible
    
    def move(self, y):
        self.pt[1] += y
        self.text.pt[1] += y

class SingleSelectButton(Button):
    def __init__(self, text: Text, rect: Rect, value, hoverEffect: str | None = None):
        super().__init__(text, rect, value, hoverEffect, "input")
        self.selected = False
        self.others: list[SingleSelectButton] = []
        self.currentValue = None

    def draw(self, win):
        super().draw(win)
    
    def setSelected(self, selected):
        if not selected == self.selected:
            self.selected = selected

            tempColor = self.rect.color
            self.rect.color = self.text.color
            self.text.color = tempColor

            self.text.rerender()

            if self.hoverEffect == "white":
                self.hoverEffect = "dark"
            elif self.hoverEffect == "dark":
                self.hoverEffect = "white"
    
    def setHover(self, hover):
        super().setHover(hover)
    
    def setOthers(self):
        self.setSelected(True)
        self.currentValue = self.value
        for button in self.others:
            button.setSelected(False)
            button.currentValue = self.value

class FileBrowser(Button):
    imageFiles = ["*.jpg", "*.jpeg", "*.jpe", "*.png", "*.bmp", "*.dib", "*.webp", "*.avif", "*.pbm", "*.pgm", "*.ppm", "*.pxm", "*.pnm", "*.pfm", "*.sr", "*.ras", "*.tiff", "*.tif", "*.exr", "*.hdr", "*.pic"]
    videoFiles = ["*.mp4", "*.avi", "*.mov", "*.mkv"]
    def __init__(self, text: Text, rect: Rect, value, hoverEffect: str | None = None):
        super().__init__(text, rect, value, hoverEffect, "filename")
        self.filePath = ""
        self.label_file_explorer = None
        self.currentFileType = None
    
    def setCurrentType(self, currentType):
        self.currentFileType = currentType
        self.setHoverEffect()
    
    def browseFiles(self):
        if self.currentFileType == "image":
            fileTypeList = (("Image Files", FileBrowser.imageFiles), ("Video Files", FileBrowser.videoFiles))
        elif self.currentFileType == "video":
            fileTypeList = (("Video Files", FileBrowser.videoFiles), ("Image Files", FileBrowser.imageFiles))
        else:
            return None
        
        filename = filedialog.askopenfilename(initialdir = str(os.getcwd()), title = "Select a File", filetypes = fileTypeList)
        
        self.filePath = filename

        return None

    def setHoverEffect(self):
        if self.currentFileType == "image" or self.currentFileType == "video":
            self.hoverEffect = "white"
        else:
            self.hoverEffect = "red"

class CheckMark(Button):
    def __init__(self, text: Text, rect: Rect, value, image: Image, displacement: int, setting: str):
        super().__init__(text, rect, value, None)
        self.image = image
        self.displacement = displacement
        self.setting = setting
    
    def draw(self, win):
        super().draw(win)
        if self.value:
            self.image.draw(win)
    
    def centerX(self, x, w):
        width = self.text.get_width() + self.displacement + self.rect.w
        self.text.pt[0] = x + w / 2 - width / 2
        self.rect.pt[0] = self.text.pt[0] + self.text.get_width() + self.displacement
        self.image.pt[0] = self.text.pt[0] + self.text.get_width() + self.displacement + self.rect.width
    
    def flipValue(self):
        self.value = not self.value
    
    def setSetting(self, buttons):
        match(self.setting):
            case "save":
                for button in buttons:
                    if isinstance(button, TextInput):
                        button.setSave(self.value)
            case "blur":
                for button in buttons:
                    if ((isinstance(button, Button) and button.setting == self.setting) or (isinstance(button, Slider) and button.settingsKey == self.setting)) and button is not self:
                        button.setPossible(self.value)
            case _:
                pass

    def move(self, y):
        super().move(y)
        self.image.pt[1] += y

class StateButton(Button):
    def __init__(self, text: Text, rect: Rect, value, hoverEffect):
        super().__init__(text, rect, value, hoverEffect)
    
    def checkConditions(self, buttons):
        inputType = getSingleSelectValue(buttons)

        if inputType is None:
            return False
        
        inputType = inputType.lower()

        if inputType == "image" or inputType == "video":
            filePath = getFilePath(buttons)
            print(inputType, filePath)
            if filePath is not None and not filePath == "":
                return True
            else:
                return False
        else:
            return True
    
    def setHover(self, hover):
        return super().setHover(hover)
    
    def changeState(self, args: dict) -> CustomThread | None:
        if args["input"] == "image":
            start_args = cv2.imread(args["path"])
            start_fn = face_swap.image_detection
        elif args["input"] == "video":
            start_args = cv2.VideoCapture(args["path"])
            start_fn = face_swap.video_detection
        elif args["input"] == "camera":
            start_args = cv2.VideoCapture(0)
            start_fn = face_swap.video_detection
        else:
            return None

        if self.value == "live":
            thread = CustomThread(args, start_fn, start_args)
            thread.start()
            return thread
        else:
            return self.value


class TextInput(Rect):
    def __init__(self, pt, w, h, color: str, font, textColor: str, setting: str, width: int = 0, borderRadius: int = 0):
        super().__init__(pt, w, h, color, width, borderRadius)
        self.save = False
        self.selected = False
        self.empty = True
        self.possible = True
        self.font = font
        self.setting = setting
        self.textColor = colors[textColor]
        self.text = "Filename"
        self.text_render = self.font.render(self.text, True, self.textColor)

    def draw(self, win):
        if self.save:
            super().draw(win)
            win.blit(self.text_render, [self.pt[0] + 5, self.pt[1] + self.h / 2 - self.text_render.get_height()])
    
    def setSave(self, save):
        self.save = save
    
    def setSelected(self, selected):
        if self.save:
            if not self.selected == selected:
                tempColor = self.color
                self.color = self.textColor
                self.textColor = tempColor
                if self.empty and selected:
                    self.text = ""
                elif self.empty and not selected:
                    self.text = "Filename"
                self.rerender()
            self.selected = selected

    def collide(self, hb):
        return (
			self.pt[0] < hb.pt[0] + hb.w
			and hb.pt[0] < self.pt[0] + self.w
			and self.pt[1] < hb.pt[1] + hb.h
			and hb.pt[1] < self.pt[1] + self.h
		)

    def setHover(self, temp):
        return
    
    def rerender(self):
        self.text_render = self.font.render(self.text, True, self.textColor)
    
    def move(self, y):
        self.pt[1] += y
    
class Slider:
    def __init__(self, pt: tuple[int, int], w: int, h: int, setting: str, settingsKey: str, font: pygame.font.Font, minVal: int = 0, maxVal: int = 100, step: int or float = 0, color: str = "#c8c8c8", handleColor = "#000000", initial: int or None = None, roundDig: int = 0, handleRadius: int or None = None, circleHandle: bool = True):
        self.pt = pt
        self.w = w
        self.h = h
        self.settingsKey = settingsKey
        self.setting = setting
        self.minVal = minVal
        self.maxVal = maxVal
        self.step = step
        self.color = color
        self.handleColor = handleColor
        self.roundDig = roundDig
        if initial is None:
            self.initial = (minVal + maxVal) / 2
        else:
            self.initial = initial
        self.value = self.initial
        self.handleRadius = handleRadius
        self.horizontal = self.w == max(self.w, self.h)

        self.selected = False

        width = 0
        borderRadius = int(min(self.w, self.h) / 8)
        self.circleHandle = circleHandle
        if circleHandle:
            if handleRadius is None:
                self.handleRadius = h / 1.3
            else:
                self.handleRadius = handleRadius
            
            # draw objects
            circlePt = [self.pt[0] + w * (self.value / self.maxVal), self.pt[1] + self.h / 2]
            self.handle = Circle(circlePt, self.handleColor, self.handleRadius)
        else:
            if self.horizontal:
                w = self.w * (self.value / self.maxVal)
                h = self.h
            else:
                w = self.w
                h = self.h * (self.value / self.maxVal)
            self.handle = Rect([self.pt[0], self.pt[1]], w, h, self.handleColor, width, borderRadius)

        borderRadius = int(min(self.w, self.h) / 8)
        self.rect = Rect([int(self.pt[0]), int(self.pt[1])], self.w, self.h, self.color, width, borderRadius)
        
        self.textBG = Rect([self.pt[0] - 50 - 10, self.pt[1]], 50, self.h, self.color, width, borderRadius)
        self.text = Text([0, 0], str(self.value), font, self.handleColor)

        self.text.centerX(self.textBG.pt[0], self.textBG.w)
        self.text.centerY(self.textBG.pt[1], self.textBG.h)

        self.surface = pygame.Surface((self.textBG.w + 10 + self.rect.w, self.rect.h), pygame.SRCALPHA)
        self.surface.fill(colors["transparent"])
        self.possible = True
    
    def move(self, y):
        self.pt[1] += y
        self.rect.pt[1] += y
        self.text.pt[1] += y
        self.textBG.pt[1] += y
        self.handle.pt[1] += y

    def draw(self, win):
        self.rect.draw(win)
        self.handle.draw(win)
        
        self.textBG.draw(win)
        self.text.draw(win)

        if not self.possible:
            win.blit(self.surface, self.textBG.pt)

    def setPossible(self, possible: bool) -> None:
        if not self.possible == possible:
            self.possible = possible
    
    def setVal(self):
        if self.roundDig == 0:
            self.value = int(self.value)
        self.text.text_render = self.text.render(str(self.value))
        self.text.centerX(self.textBG.pt[0], self.textBG.w)
        self.text.centerY(self.textBG.pt[1], self.textBG.h)
        
    def setHover(self, temp):
        return

    def increment(self) -> None:
        if self.value + self.step < self.maxVal:
            self.value += self.step
        elif not self.value > self.maxVal and self.value + self.step >= self.maxVal:
            self.value = self.maxVal
        
        self.calcHandlePos()
        
    def decrement(self) -> None:
        if self.value - self.step > self.minVal:
            self.value -= self.step
        elif not self.value < self.minVal and self.value - self.step <= self.minVal:
            self.value = self.minVal
    
        self.calcHandlePos()

    def calcHandlePos(self):
        if self.horizontal:
            if not self.circleHandle:
                self.handle.w = (self.value / self.maxVal) * self.w
            else:
                self.handle.pt[0] = self.pt[0] + (self.value / self.maxVal) * self.w
        else:
            if not self.circleHandle:
                self.handle.h = (self.value / self.maxVal) * self.h
            else:
                self.handle.pt[1] = self.pt[1] + (self.value / self.maxVal) * self.h
    
    def slide(self, hb) -> None:
        if self.horizontal:
            x = hb.pt[0] - self.pt[0]
            self.value = round(x / self.w * self.maxVal, self.roundDig)
            if not self.circleHandle:
                self.handle.w = x
            else:
                self.handle.pt = (hb.pt[0], self.handle.pt[1])
        else:
            y = hb.pt[1] - self.pt[1]
            self.value = round(y / self.h * self.maxVal, self.roundDig)
            if not self.circleHandle:
                self.handle.h = y
            else:
                self.handle.pt = (self.handle.pt[0], hb.pt[1])
        self.setVal()
    
    def checkBoundaries(self, hb):
        return (
			self.pt[0] < hb.pt[0] + hb.w
			and hb.pt[0] < self.pt[0] + self.w
			and self.pt[1] < hb.pt[1] + hb.h
			and hb.pt[1] < self.pt[1] + self.h
		)

    def collide(self, hb) -> bool:
        if self.checkBoundaries(hb) and self.possible and self.selected:
            self.active = True
            self.slide(hb)
            return True
        elif self.checkBoundaries(hb) and self.possible and not self.selected:
            return True
        
        return False
    
def getSingleSelectValue(buttons):
    for button in buttons:
        if isinstance(button, SingleSelectButton):
            return button.currentValue

def getFilePath(buttons):
    for button in buttons:
        if isinstance(button, FileBrowser):
            return button.filePath