from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

# NFR-005、AI-11：只接受 JPEG、PNG、WebP，單張最多 5 MB
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024


def validate_image(file):
    """檢查上傳的圖片。用 Pillow 讀取實際格式，不只看副檔名（research R-07）。"""
    if file.size > MAX_IMAGE_BYTES:
        raise ValidationError("圖片不能超過 5 MB。")

    position = file.tell() if hasattr(file, "tell") else None
    try:
        file.seek(0)
        with Image.open(file) as image:
            image_format = image.format
            image.verify()
    except (UnidentifiedImageError, OSError, SyntaxError):
        raise ValidationError("無法辨識的圖片檔，只接受 JPEG、PNG、WebP。")
    finally:
        file.seek(position or 0)

    if image_format not in ALLOWED_IMAGE_FORMATS:
        raise ValidationError("只接受 JPEG、PNG、WebP 格式的圖片。")
