# utils.py

from playwright.sync_api import sync_playwright
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles
from lib.Highlighted_Code import Highlighted_Code

def take_screenshot_from_url(url, session_data, target_style_name):
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch()
        browser_context = browser.new_context(device_scale_factor=2)
        browser_context.add_cookies([session_data])
        page = browser_context.new_page()
        page.goto(url)
        screenshot_bytes = page.locator(".code."+target_style_name).screenshot()
        browser.close()
        return screenshot_bytes
    
def create_styled_codes(code) -> []:
    styled_codes = []
    style_list = get_all_styles()

    for style in style_list:
        formatter = HtmlFormatter(style=style, classprefix=style, cssclass='code')
        formatter.cssstyles = 'background-color:' + formatter.style.background_color
        styled_codes.append(highlight(
            code, Python3Lexer(), formatter)
        )
    return styled_codes

def get_all_style_definitions() -> []:
    all_defs = []
    style_list = get_all_styles()
    for style in style_list:
        all_defs.append(HtmlFormatter(style=style, classprefix=style).get_style_defs())
    
    return all_defs

def get_all_background_colors() -> []:
    all_bg = []
    style_list = get_all_styles()
    for s in style_list:
        all_bg.append(HtmlFormatter(style=s,).style.background_color)

    return all_bg

def generate_highlighted_codes(code) -> []:
    codes_list = []
    style_list = get_all_styles()
    
    for s in style_list:
        codes_list.append(Highlighted_Code(code, s))

    return codes_list