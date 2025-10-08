from flask import Blueprint,redirect,render_template,url_for,jsonify,flash


auth_bp = Blueprint("auth",__name__,template_folder="templates",static_folder="static",static_url_path="/")


# --- RENDER TEMPLATES ONLY ----
@auth_bp.route("/register_or_login_lecturer", methods=["GET"])
def register_or_login_lecturer():
    return render_template("auth/lecturer_auth.html")


@auth_bp.route("/register_or_login_student", methods=["GET"])
def register_or_login_student():
    return render_template("auth/student_auth.html")

# ----- REGISTER OR LOGIN LECTURER  LOGIC ---
@auth_bp.route("/register_lecturer", methods=["POST"])
def register_lecturer():
    return "register lecture"

@auth_bp.route("/login_lecturer", methods=["POST"])
def login_lecturer():
   return "login lecture"

# ----- REGISTER OR LOGIN STUDENT  LOGIC ----
@auth_bp.route("/register_student", methods=["POST"])
def register_student():
    return "register student" 


@auth_bp.route("/login_student", methods=["POST"])
def student_login():
    return "login student" 
      