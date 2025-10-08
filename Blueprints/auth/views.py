from flask import Blueprint, jsonify, request
from Blueprints.auth.models import User, TokenBlockList
from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt,jwt_required,get_jwt_identity
from extensions import db

# create a blueprint called "auth" and set the import name
auth_bp = Blueprint('auth',__name__)


@auth_bp.post('/register')
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message":"No data submitted"}), 400
    
    # extract data
    username = data['username']
    password = data['password']

    print("Username:", username)  # Debugging
    print("Password:", password)  # Debugging
    print("Password Type:", type(password))  # Debugging

    # validate password: ensure it only a 4 digit
    if not password.isdigit() or len(password) != 4:
        return jsonify({"message":"Password must be exactly 4 digits"}), 400
    
    # check if user already exists, before creating new user
    existing_user = User.query.filter(User.username == username).first()

    if existing_user is not None:
        return jsonify({"message":"Username already taken"}), 403
    
   
    
    try:
        # user does not exist and new user can be created
        new_user = User(username=username,password=password)
        # save new user to database
        new_user.save_user()
        return jsonify({"message":"User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 400
    finally:
        db.session.close()




@auth_bp.post('/login') # type: ignore
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message":"No data submitted"}), 400
    
    missing_fields = []

    if "username" not in data:
        missing_fields.append('username')

    if "password" not in data:
        missing_fields.append('password')


    # if there are missing fields
    if missing_fields:
        return jsonify({
            "message":"Missing required fields",
            "missing fields": ','.join(missing_fields)
        }), 400 



    username=data.get('username')
    password=data.get('password')

    print(username,password)
   

#  check if user exists
    try:
        user = User.get_user_username(username=username)

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            
            return jsonify(
                {
                    "message": "User logged in successfully",
                    "tokens": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    }
                }
                ), 200  
        return jsonify({"message":"invalid password or username"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400   
      

@auth_bp.get('/regain_access')   
@jwt_required(refresh=True)  
def regain_access():
    identity = get_jwt_identity()
    
    # create new access token
    access_token = create_access_token(identity=identity)

    return jsonify({"current user":identity, "access token":access_token}), 200 


@auth_bp.get('/logout')
# if verify_type=True, only access token. 
# if verify_type=False, access and refresh token token. 
@jwt_required(verify_type=False)
def logout_user():

    jwt = get_jwt()

    jti = jwt['jti']
    token_type=jwt['type']

    try:
        token = TokenBlockList(jti=jti)
        token.save_blocklisted_token()
        return jsonify({"message": f"{token_type} token revoked successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 200
    finally:
        db.session.close()






          

    


