from flask import Flask, request, jsonify
import mysql.connector
import re
from config import USER, PASSWORD, HOST

app = Flask(__name__)
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database="task_colorifix"
)

# Endpoint for adding a company
@app.route("/company", methods=["POST"])
def add_company():
    company_name = request.json.get("company_name")

    if not company_name:
        return jsonify({"error": "Company name is required."}), 400

    cursor = conn.cursor()

    # Check if company already exists in the database
    cursor.execute("SELECT CompanyName FROM Companies WHERE CompanyName = %s", (company_name,))
    company = cursor.fetchone()
    if company:
        return jsonify({"error": "Cannot add the Company. Company already exists."}), 409
    
    cursor.execute("INSERT INTO Companies (CompanyName) VALUES (%s)", (company_name,))
    conn.commit()
    cursor.close()

    return jsonify({"message": "Company added successfully."}), 201

# Endpoint for adding a permission group
@app.route("/permission-group", methods=["POST"])
def add_permission_group():
    permission_group_name = request.json.get("permission_group_name")
    permission_name = request.json.get("permission_name")
    access_level = request.json.get("access_level")

    if not (permission_group_name and permission_name):
        return jsonify({"error": "Permission group name and permission name are required."}), 400

    cursor = conn.cursor()

    # Check if company already exists in the database
    cursor.execute("SELECT PermissionGroupName FROM PermissionGroups WHERE PermissionGroupName = %s", (permission_group_name,))
    permission_group = cursor.fetchone()
    if permission_group:
        return jsonify({"error": "Cannot add the Permission Group. Permission Group already exists."}), 409
    
    cursor.execute("INSERT INTO PermissionGroups (PermissionGroupName, PermissionNameDescription) VALUES (%s, %s)",
                   (permission_group_name, permission_name))
    conn.commit()
    cursor.close()

    return jsonify({"message": "Permission group added successfully."}), 201

# Endpoint for adding a user
@app.route("/user", methods=["POST"])
def add_user():
    username = request.json.get("username")
    company_name = request.json.get("company_name")
    permission_group_name = request.json.get("permission_group_name")

    if not (username and company_name and permission_group_name):
        return jsonify({"error": "Username, company name, and permission group name are required."}), 400

    # Validate username as a valid email address
    if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
        return jsonify({"error": "Invalid email address"}), 400
    
    cursor = conn.cursor()

    # Check if user already exists in the database
    cursor.execute("SELECT UserName FROM Users WHERE UserName = %s", (username,))
    company = cursor.fetchone()
    if company:
        return jsonify({"error": "The username alsready exists."}), 409
    
    # Check if the company exists in db
    cursor.execute("SELECT CompanyName FROM Companies WHERE CompanyName = %s", (company_name,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Company does not exist."}), 404

    # Check if the permission group exists in db
    cursor.execute("SELECT PermissionGroupName FROM PermissionGroups WHERE PermissionGroupName = %s",
                   (permission_group_name,))
    permission_group = cursor.fetchone()
    if not permission_group:
        return jsonify({"error": "Permission group does not exist."}), 404

    cursor.execute("INSERT INTO Users (UserName, PermissionGroupName, CompanyName) VALUES (%s, %s, %s)",
                   (username, permission_group_name, company_name))
    conn.commit()
    cursor.close()

    return jsonify({"message": "User added successfully."}), 201

# Endpoint for editing an existing user
@app.route("/user/<username>", methods=["PUT"])
def edit_user(username):
    permission_group_name = request.json.get("permission_group_name")

    if not permission_group_name:
        return jsonify({"error": "Permission group name is required."}), 400

    cursor = conn.cursor()
    # Check if the user exists
    cursor.execute("SELECT UserName FROM Users WHERE UserName = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "User does not exist."}), 404

    # Check if the permission group exists in db
    cursor.execute("SELECT PermissionGroupName FROM PermissionGroups WHERE PermissionGroupName = %s",
                   (permission_group_name,))
    permission_group = cursor.fetchone()
    if not permission_group:
        return jsonify({"error": "Permission group does not exist."}), 404
    
    cursor.execute("UPDATE Users SET PermissionGroupName = %s WHERE UserName = %s",
                   (permission_group_name, username))
    conn.commit()
    cursor.close()

    return jsonify({"message": "User updated successfully."})

# Endpoint for returning a list of users with pagination
@app.route("/users", methods=["GET"])
def get_users():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users LIMIT %s OFFSET %s", (per_page, (page - 1) * per_page))
    users = cursor.fetchall()
    cursor.close()

    user_list = []
    for user in users:
        user_dict = {
            "username": user[0],
            "permission_group": user[1],
            "company": user[2]
        }
        user_list.append(user_dict)

    return jsonify({"users": user_list})


if __name__ == "__main__":
    app.run()
