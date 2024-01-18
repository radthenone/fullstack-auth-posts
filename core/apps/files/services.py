import base64
import uuid
from io import BytesIO
from typing import Optional

import filetype
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


class ImageService:
    ALLOWED_TYPES = ["png", "jpg"]

    def __init__(self, data: Optional[str]):
        self.file_mime_type = None
        self.thumbnail_values = None
        if not data:
            raise ValueError("Data is required.")
        self.to_format, self.file_mime_type, self.data = self.basic_instances(data)

    @staticmethod
    def basic_instances(data):
        if isinstance(data, str) and data.startswith("data:image"):
            header, data = data.split(";base64,")
            file_mime_type = header.replace("data:", "")
            to_format = file_mime_type.split("/")[1].upper()
            return to_format, file_mime_type, data
        else:
            raise ValueError("Data must be an base64-encoded string.")

    def decoded_file(self, base64_data: str):
        _, _, base64_data = self.basic_instances(data=base64_data)
        try:
            file = base64.b64decode(base64_data)
            return file
        except ValueError as error:
            raise ValidationError(f"Invalid base64 data: {error}")

    @staticmethod
    def get_file_extension(decoded_file):
        extension = filetype.guess_extension(decoded_file)
        if extension is None:
            try:
                image = Image.open(BytesIO(decoded_file))
            except (ImportError, OSError):
                raise ValidationError("Invalid image format.")
            else:
                extension = image.format.lower()

        return "jpg" if extension == "jpeg" else extension

    def create_simple_file(self, base64_data: str, method: str):
        decoded_file = self.decoded_file(base64_data=base64_data)

        file_name = self.get_file_name(
            method=method,
        )
        file_extension = self.get_file_extension(decoded_file=decoded_file)

        if file_extension not in self.ALLOWED_TYPES:
            raise ValidationError("""Invalid type. This is not an image.""")

        complete_file_name = file_name + "." + file_extension

        return SimpleUploadedFile(
            name=complete_file_name,
            content=decoded_file,
            content_type=self.file_mime_type,
        )

    def resize_image(self, size: Optional[tuple[int, int]]) -> SimpleUploadedFile:
        if not size:
            raise ValueError("Size is required.")
        img = self.base64_to_image(data=self.data)
        resized_img = img.resize(size=size, resample=Image.LANCZOS)
        base64_data = self.image_to_base64(image=resized_img, to_format=self.to_format)
        return self.create_simple_file(
            base64_data=base64_data,
            method=self.__class__.resize_image.__name__,
        )

    def thumbnail_image(self, size: Optional[tuple[int, int]]):
        if not size:
            raise ValueError("Size is required.")
        self.thumbnail_values = size
        img = self.base64_to_image(data=self.data)
        img.thumbnail(size=size, resample=Image.LANCZOS)
        base64_data = self.image_to_base64(image=img, to_format=self.to_format)
        return self.create_simple_file(
            base64_data=base64_data,
            method=self.__class__.thumbnail_image.__name__,
        )

    def crop_image(self, box: Optional[tuple[int, int, int, int]]):
        if not box:
            raise ValueError("Box is required.")
        img = self.base64_to_image(data=self.data)
        img = img.crop(box=box)
        base64_data = self.image_to_base64(image=img, to_format=self.to_format)
        return self.create_simple_file(
            base64_data=base64_data,
            method=self.__class__.crop_image.__name__,
        )

    def get_file_name(self, method: str):
        if method == "thumbnail_image":
            return f"thumbnail/{self.thumbnail_values[0]}x{self.thumbnail_values[1]}/{uuid.uuid4()}"
        else:
            return f"{uuid.uuid4()}"

    @staticmethod
    def base64_to_image(data: str) -> Image.Image:
        if isinstance(data, str) and data.startswith("data:image"):
            _, data = data.split(";base64,")
        img_data = BytesIO(base64.b64decode(data))
        img = Image.open(img_data)
        return img

    @staticmethod
    def image_to_base64(image: Image, to_format=None) -> str:
        if to_format is None:
            to_format = image.format.upper() or "PNG"
        img_data = BytesIO()
        image.save(img_data, format=to_format)
        img_str = base64.b64encode(img_data.getvalue()).decode("utf-8")
        return f"data:image/{to_format.lower()};base64,{img_str}"
