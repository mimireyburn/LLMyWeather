#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from inky import InkyWHAT
import time
import os

class Visualise(object): 
    
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # Write a function to wrap text to the specified width on InkypWHAT
    def _wrap_text(self, text, width, font):
        text_lines = []
        text_line = []
        text_words = text.split()
        for word in text_words:
            if font.getsize(' '.join(text_line + [word]))[0] <= (width-20):
                text_line.append(word)
            else:
                if text_line:
                    text_lines.append(' '.join(text_line))
                text_line = [word]
        if text_line:
            text_lines.append(' '.join(text_line))
        return text_lines

    def draw(self, message, style):

        current_path = os.getcwd()
        font = ImageFont.truetype(current_path + "/files/AtkinsonHyperlegible-Regular.ttf", size=20)

        img = Image.new('RGB', (self.width, self.height), color='white')
        imgDraw = ImageDraw.Draw(img)

        # Wrap text to width of display
        textLines = self._wrap_text(message, self.width, font)

        # Calculate y position to centre text on display (multi-line)
        textHeight = font.getsize_multiline(message)[1] 

        # Calculate total text height for all lines to centre vertically
        totalTextHeight = len(textLines) * textHeight
        yText = (self.height - totalTextHeight) // 2

        # Draw text on image
        for line in textLines:
            textWidth = font.getsize(line)[0]
            xText = (self.width - textWidth) // 2
            imgDraw.text((xText, yText), line, font=font, fill=(0, 0, 0))
            yText += textHeight  # Move y down for the next line

        # Add style in bottom right corner followed by weather logo
        styleWidth, styleHeight = imgDraw.textsize(style, font=font)
        xStyle = self.width - styleWidth - 10 - 50
        yStyle = self.height - styleHeight - 10

        imgDraw.text((xStyle, yStyle), style, font=font, fill=(0, 0, 0))
        
        # Add weather logo

        current_path = os.getcwd()
        logo = Image.open(current_path + '/files/weather_logo.png')
        logo = logo.resize((50, 50))

        logo_bg = Image.new('RGBA', logo.size, (255, 255, 255, 255))
        logo_with_bg = Image.alpha_composite(logo_bg, logo)
        img.paste(logo_with_bg, (self.width - 50, self.height - 50), mask=logo_with_bg.split()[3])

        img.save(current_path + '/files/weather.png')
    
    def display(self, colour):
        inky_display = InkyWHAT(colour)
        inky_display.set_border(inky_display.WHITE)
        # convert image 
        current_path = os.getcwd()
        img = Image.open(current_path + "/files/weather.png")

        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

        img = img.convert("RGB").quantize(palette=pal_img)

        # display image
        inky_display.set_image(img)
        inky_display.show()
        

        
