import os

from PIL import Image
from io import BytesIO
from django.db import models

from django.core.files.base import ContentFile



def convert_to_webp(image_path, quality=80):
    img = Image.open(image_path)
    img = img.convert("RGB")  # Ensure RGB format for WebP
    webp_image = BytesIO()
    img.save(webp_image, "webp", quality=quality)
    webp_image.seek(0)
    return webp_image


class WebpImageField(models.ImageField):
    def save(self, name, content, save=True):
        file_name, ext = os.path.splitext(name)
        webp_image = convert_to_webp(content, quality=80)
        name = f"{file_name}.webp"
        content = ContentFile(webp_image.read())
        return super().save(name, content, save)
