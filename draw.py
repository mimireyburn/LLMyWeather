from PIL import Image, ImageDraw, ImageFont

width = 400
height = 300
message = "Weather goes here"
font = ImageFont.truetype("/Library/fonts/Arial.ttf", size=30)

img = Image.new('RGB', (width, height), color='white')

imgDraw = ImageDraw.Draw(img)

textWidth, textHeight = imgDraw.textsize(message, font=font)
xText = (width - textWidth) / 2
yText = (height - textHeight) / 2

imgDraw.text((xText, yText), message, font=font, fill=(0, 0, 0))

img.save('weather.png')