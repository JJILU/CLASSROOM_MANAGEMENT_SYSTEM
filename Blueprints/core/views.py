from flask import Blueprint,render_template


core_bp = Blueprint("core",__name__,template_folder="templates",static_folder="static",static_url_path="/")

@core_bp.route("/", methods=["GET"])
def landing_page():
    return render_template("core/landing_page.html")
