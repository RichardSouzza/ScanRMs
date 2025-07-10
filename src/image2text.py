import os
from glob import glob

from PIL import Image
from pytesseract import image_to_string


def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    text = image_to_string(image, lang="por")
    return text


images = glob(os.path.join("..\\images", "*.png"))

for image in images:
    text = extract_text_from_image(image)
    print(text)
