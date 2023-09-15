# Please just trust it works (we think)
# TODO: comments, comments, comments
# TODO: either use type hints or don't

import pygame
import tkinter
from tkinter import filedialog
import os
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
    "nord16": "#B48EAD"
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
    def __init__(self, text: Text, rect: Rect, value, hoverEffect: str | None = None):
        super().__init__(rect.pt, rect.w, rect.h)
        self.text = text
        self.rect = rect
        self.value = value
        self.hoverEffect = hoverEffect
        self.hover = False
    
    def draw(self, win):
        self.rect.draw(win)
        self.text.draw(win)
        if self.hover and self.hoverEffect is not None:
            hoverEffects[self.hoverEffect].draw(win, self.rect)
    
    def collide(self, hb):
        return (
			self.pt[0] < hb.pt[0] + hb.w
			and hb.pt[0] < self.pt[0] + self.w
			and self.pt[1] < hb.pt[1] + hb.h
			and hb.pt[1] < self.pt[1] + self.h
		)
    
    def setHover(self, hover):
        self.hover = hover

class SingleSelectButton(Button):
    def __init__(self, text: Text, rect: Rect, value, hoverEffect: str | None = None):
        super().__init__(text, rect, value, hoverEffect)
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
        super().__init__(text, rect, value, hoverEffect)
        self.filePath = ""
        self.label_file_explorer = None
        self.currentFileType = None
    
    def setCurrentType(self, currentType):
        self.currentFileType = currentType
        self.setHoverEffect()
    
    def browseFiles(self):
        if self.currentFileType == "Image":
            fileTypeList = (("Image Files", FileBrowser.imageFiles), ("Video Files", FileBrowser.videoFiles))
        elif self.currentFileType == "Video":
            fileTypeList = (("Video Files", FileBrowser.videoFiles), ("Image Files", FileBrowser.imageFiles))
        else:
            return None
        
        filename = filedialog.askopenfilename(initialdir = str(os.getcwd()), title = "Select a File", filetypes = fileTypeList)
        
        self.filePath = filename

        return None

    def setHoverEffect(self):
        if self.currentFileType == "Image" or self.currentFileType == "Video":
            self.hoverEffect = "white"
        else:
            self.hoverEffect = "red"

class CheckMark(Button):
    def __init__(self, text: Text, rect: Rect, value, image: Image, displacement: int):
        super().__init__(text, rect, value, None)
        self.image = image
        self.displacement = displacement
    
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

class StateButton(Button):
    def __init__(self, text: Text, rect: Rect, value, hoverEffect):
        super().__init__(text, rect, value, hoverEffect)

class TextInput(Rect):
    def __init__(self, pt, w, h, color: str, font, textColor: str, width: int = 0, borderRadius: int = 0):
        super().__init__(pt, w, h, color, width, borderRadius)
        self.save = False
        self.selected = False
        self.empty = True
        self.font = font
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