import io

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from PIL import Image

from apps.catalog.validators import MAX_IMAGE_BYTES, validate_image


def make_image(fmt, name, size=(10, 10)):
    buf = io.BytesIO()
    Image.new("RGB", size, "white").save(buf, format=fmt)
    return SimpleUploadedFile(name, buf.getvalue(), content_type=f"image/{fmt.lower()}")


class ValidateImageTests(SimpleTestCase):
    """NFR-005、AI-11：只接受 JPEG、PNG、WebP，單張最多 5 MB。"""

    def test_accepts_jpeg_png_webp(self):
        for fmt, name in [("JPEG", "a.jpg"), ("PNG", "a.png"), ("WEBP", "a.webp")]:
            with self.subTest(fmt=fmt):
                validate_image(make_image(fmt, name))

    def test_rejects_file_over_5_mb(self):
        upload = make_image("PNG", "big.png")
        upload.size = MAX_IMAGE_BYTES + 1
        with self.assertRaisesMessage(ValidationError, "5 MB"):
            validate_image(upload)

    def test_rejects_text_file_renamed_to_jpg(self):
        upload = SimpleUploadedFile("fake.jpg", b"not an image at all", content_type="image/jpeg")
        with self.assertRaises(ValidationError):
            validate_image(upload)

    def test_rejects_gif(self):
        with self.assertRaises(ValidationError):
            validate_image(make_image("GIF", "a.gif"))
