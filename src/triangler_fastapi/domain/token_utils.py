import secrets
from datetime import datetime
from datetime import timedelta

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.svg import SvgPathImage

from triangler_fastapi.config import HOST_NAME
from triangler_fastapi.config import OBSERVATION_TOKEN_EXPIRY_DAYS
from triangler_fastapi.config import OBSERVATION_TOKEN_LENGTH


def generate_unique_token() -> str:
    return secrets.token_urlsafe(OBSERVATION_TOKEN_LENGTH)


def calculate_expiry_date(n_days: int = OBSERVATION_TOKEN_EXPIRY_DAYS) -> datetime:
    return datetime.now() + timedelta(days=n_days)


def generate_qr_code_svg(token: str) -> bytes:
    qrcode_url = f"https://{HOST_NAME}/observation/response/{token}"
    qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_H)
    qr.add_data(qrcode_url)
    return qr.make_image(
        image_factory=SvgPathImage, module_drawer=RoundedModuleDrawer
    ).to_string()


def generate_qr_code_png(token: str) -> StyledPilImage:
    qrcode_url = f"https://{HOST_NAME}/observation/response/{token}"
    qr = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_H)
    qr.add_data(qrcode_url)
    return qr.make_image(
        image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer
    )
