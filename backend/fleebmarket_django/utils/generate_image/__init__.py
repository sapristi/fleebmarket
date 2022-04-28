import random
import subprocess

from html2image import Html2Image

from .static import palettes, template, texts


def get_html():
    text = random.choice(texts)
    palette = random.choice(palettes)
    html = template.format(
        background_color=palette[0], text_color=palette[3], text=text
    )
    return html


def make_hti(size, output_path):

    return Html2Image(
        chrome_path=os.environ.get("CHROME_PATH", "/usr/bin/chromium"),
        size=size,
        output_path=output_path,
        custom_flags=["--disable-gpu"],
    )


def generate_image(chrome_path, size, output_path, name):

    hti = Html2Image(chrome_path=chrome_path, size=size, output_path=output_path)

    text = random.choice(texts)
    palette = random.choice(palettes)

    html = template.format(
        background_color=palette[0], text_color=palette[3], text=text
    )

    hti.screenshot(html_str=html, save_as=name)
