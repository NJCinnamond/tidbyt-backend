from PIL import Image, ImageDraw, ImageFont
import io
import base64

TIDBYT_RESOLUTION = (64, 32)


class ImageService:
    def generate_pil_from_base_64(self, img_data: str) -> object:
        img_data = img_data.split(",")[1]
        img_data = base64.b64decode(img_data)
        img_data = io.BytesIO(img_data)
        img = Image.open(img_data)
        cropped_img = self.scale_img_for_tidbyt(img)

        blob = io.BytesIO()
        cropped_img.save(blob, format="PNG")
        return blob

    def generate_base_64_from_pil(self, img: object) -> str:
        img_base64 = base64.b64encode(img.read())
        img_base64 = img_base64.decode("utf-8")
        return img_base64

    def generate_pil_from_text(self, text: str) -> object:
        img = Image.new("RGB", TIDBYT_RESOLUTION, color="black")
        canvas = ImageDraw.Draw(img)
        canvas.multiline_text((0, 10), text, fill="#FFFFFF")

        blob = io.BytesIO()
        img.save(blob, format="PNG")
        return blob

    def scale_img_for_tidbyt(self, img: object) -> object:
        img = img.resize(TIDBYT_RESOLUTION)
        return img
