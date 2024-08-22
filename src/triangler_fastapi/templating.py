from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape

html_env = Environment(
    loader=PackageLoader("triangler_fastapi"), autoescape=select_autoescape()
)
