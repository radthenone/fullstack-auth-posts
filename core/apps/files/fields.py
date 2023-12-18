from rest_framework import fields
from apps.files.services import ImageService
import base64
from typing import Optional


class ResizeBase64ImageField(fields.ImageField):
    def __init__(self, **kwargs):
        self.size: Optional[tuple[int, int]] = kwargs.pop("size", None)
        super().__init__(**kwargs)

    def to_internal_value(self, data: str = None):
        service = ImageService(data=data)
        data = service.resize_image(size=self.size)
        return data

    def to_representation(self, file):
        if not file:
            return ""
        try:
            with file.open() as f:
                return base64.b64encode(f.read()).decode()
        except Exception:
            raise OSError("Error encoding file")


class ThumbnailBase64ImageField(fields.ImageField):
    def __init__(self, **kwargs):
        self.size: Optional[tuple[int, int]] = kwargs.pop("size", None)
        super().__init__(**kwargs)

    def to_internal_value(self, data: str = None):
        service = ImageService(data=data)
        data = service.thumbnail_image(size=self.size)
        return data

    def to_representation(self, file):
        if not file:
            return ""
        try:
            with file.open() as f:
                return base64.b64encode(f.read()).decode()
        except Exception:
            raise OSError("Error encoding file")


class CropBase64ImageField(fields.ImageField):
    def __init__(self, **kwargs):
        self.box: Optional[tuple[int, int, int, int]] = kwargs.pop("box", None)
        super().__init__(**kwargs)

    def to_internal_value(self, data: str = None):
        service = ImageService(data=data)
        data = service.crop_image(box=self.box)
        return data

    def to_representation(self, file):
        if not file:
            return ""
        try:
            with file.open() as f:
                return base64.b64encode(f.read()).decode()
        except Exception:
            raise OSError("Error encoding file")
