from flask import Blueprint,render_template


dashboard_bp = Blueprint("dashboard",__name__,template_folder="templates",static_folder="static",static_url_path="/")

@dashboard_bp.route("/", methods=["GET"])
def landing_page():
    render_template("dashboard/landing_page.html")
