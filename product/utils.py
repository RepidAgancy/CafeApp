from PIL import Image
import tempfile
from django.core.files import File


def create_test_image():
    return File(create_api_test_image(), name="test.jpg")


def create_api_test_image():
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file