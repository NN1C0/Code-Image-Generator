from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer

class Highlighted_Code():
    code = ""
    highlighted_code = ""
    background_color = ""
    cssstyle = ""
    style_name = ""

    def __init__(self, code, style) -> None:
        self.code = code
        self.style_name = style
        formatter = HtmlFormatter(style=self.style_name, classprefix=self.style_name)
        self.cssstyle = formatter.get_style_defs()
        self.background_color = formatter.style.background_color
        self.highlighted_code = highlight(self.code, Python3Lexer(), formatter)