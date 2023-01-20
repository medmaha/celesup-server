from PIL import Image
from django.db import models

c = 0
def profile_avatar_resize(file_path, size=200):
    from PIL import Image

    # Open the image file
    image = Image.open(file_path)

    # Resize the image to a square aspect ratio
    width, height = image.size

    if width == height and width == size: return

    if width > height:
        delta = width - height
        left = int(delta/2)
        upper = 0
        right = height + left
        lower = height

    elif height > width:
        delta = height - width
        left = 0
        upper = int(delta/2)
        right = width
        lower = width + upper

    else:
        left = 0
        upper = 0
        right = width
        lower = height
    image = image.crop((left, upper, right, lower))

    # Resize the image to a specific size
    size = (size, size)
    image = image.resize(size,resample=Image.BICUBIC)

    # Save the image
    image.save(file_path)
    print(c)
    c += 1


def responsive_resize(file_path, width=450):

    new_width = width
    # Open the image file

    image = Image.open(file_path)
    # Get the original aspect ratio
    width, height = image.size

    if width <= new_width: return

    aspect_ratio = width / height

    # Calculate the new dimensions
    new_height = int(new_width / aspect_ratio)

    # Resize the image
    image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Save the image
    image.save(file_path)



