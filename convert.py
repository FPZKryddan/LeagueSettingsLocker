from PIL import Image

image = Image.open("./images/lock.png")
image.save("icon.ico", format="ICO")
