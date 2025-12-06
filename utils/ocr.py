import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

SUPPORTED_IMAGE_EXT = {'.png','.jpg','.jpeg','.tif','.tiff','.bmp'}

def image_to_text_pil(image):
    config='--psm 6'
    return pytesseract.image_to_string(image, config=config)

def pdf_to_text(path):
    texts=[]
    images=convert_from_path(path)
    for img in images:
        texts.append(image_to_text_pil(img))
    return "\n".join(texts)

def file_to_text(path):
    _,ext=os.path.splitext(path.lower())
    if ext=='.pdf': return pdf_to_text(path)
    if ext in SUPPORTED_IMAGE_EXT:
        return image_to_text_pil(Image.open(path))
    raise ValueError("Unsupported file type")
