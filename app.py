from flask import Flask, render_template, session, redirect, request, url_for, send_file
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles
import base64
import utils
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.secret_key = "2e9ac41b1e0b66a8d93d66400e2300c4b4c2953f"


PLACEHOLDER_CODE = "print('Hello, World!')"
DEFAULT_STYLE = "monokai"
NO_CODE_FALLBACK = "# No Code Entered"


@app.route("/", methods=["GET"])
def code():
    #Assign default if no prior session existed
    if session.get("code") is None:
        session["code"] = PLACEHOLDER_CODE
    
    lines = session["code"].split("\n")
    context = {
        "message": "Hand me your Python code",
        "code": session["code"],
        "num_lines": len(lines),
        "max_chars": len(max(lines, key=len)),
    }
    return render_template("code_input.html", **context)

#Saves the current user session's code
@app.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code") or NO_CODE_FALLBACK
    return redirect(url_for("code"))

#Replaces the current user session with default
@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = PLACEHOLDER_CODE
    return redirect(url_for("code"))

#Styles current session code
@app.route("/style", methods=["GET"])
def style():
    if session.get("style") is None:
        session["style"] = DEFAULT_STYLE

    formatter = HtmlFormatter(style=session["style"])
    context = {
        "message": "Select your style",
        "all_styles": list(get_all_styles()),
        "style": session["style"],
        "style_definitions": utils.get_all_style_definitions(),
        "style_bg_colors": utils.get_all_background_colors(),
        "styled_codes": utils.create_styled_codes(session["code"]),
        "highlighted_codes_list": utils.generate_highlighted_codes(session["code"]),
    }
    return render_template("style_selection.html", **context)

#Saves current style selection in session
@app.route("/save_style", methods=["POST"])
def save_style():
    if request.form.get("style") is not None:
        session["style"] = request.form.get("style")
    if request.form.get("code") is not None:
        session["code"] = request.form.get("code") or NO_CODE_FALLBACK
    return redirect(url_for("style"))

@app.route("/image", methods=["GET"])
def image():
    style_name = request.args.get("style")
    session_data = {
        "name": app.config["SESSION_COOKIE_NAME"],
        "value": request.cookies.get(app.config["SESSION_COOKIE_NAME"]),
        "url": request.host_url,
    }
    target_url = request.host_url + url_for("style")
    image_bytes = utils.take_screenshot_from_url(target_url, session_data, style_name)
    context = {
        "message": "Done! 🎉",
        "image_b64": base64.b64encode(image_bytes).decode("utf-8"),
    }

    fileObject  = BytesIO()
    image = Image.open(BytesIO(image_bytes))
    image.save(fileObject, "PNG")
    fileObject.seek(0)

    return send_file(fileObject, mimetype="PNG", as_attachment=True, download_name="Your_Code.png", )
    #return render_template("image.html", **context)

@app.route("/download_image", methods=["GET"])
def download_image():
    pass