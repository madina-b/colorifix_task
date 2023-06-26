import requests 
import mysql.connector
import shortuuid
from config import USER, PASSWORD, HOST

ENDPOINT  = "http://localhost:5000"
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database="task_colorifix"
)

def test_add_new_company():
    payload = {
        "company_name": shortuuid.uuid()  # random name of the company
    }
    company = payload["company_name"]

    add_company_res = requests.post(ENDPOINT + "/company", json=payload)
    
    # Assert that the response status code is 201 (Created)
    assert add_company_res.status_code == 201

    # Assert that the company was successfully added to the database
    assert add_company_res.json()["message"] == "Company added successfully."

    # Assert that the company is now in database
    cursor = conn.cursor()
    cursor.execute("SELECT CompanyName FROM Companies WHERE CompanyName = %s", (company,))
    company = cursor.fetchone()
    
    cursor.close()
    assert company


def test_add_company_existing():

    payload = {
        "company_name": shortuuid.uuid()  # random name of the company
    }
    company = payload["company_name"]

    add_company_res_1 = requests.post(ENDPOINT + "/company", json=payload)
    add_company_res_2 = requests.post(ENDPOINT + "/company", json=payload)
    conn.commit()
    
    # Assert that the response status code is 409 (Already exists)
    assert add_company_res_2.status_code == 409

    # Assert that the company was successfully added to the database
    assert add_company_res_2.json()["error"] == "Cannot add the Company. Company already exists."

    # Assert that single record of the company exists in database
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM Companies WHERE CompanyName = %s", (company,))
    (company_count, )= cursor.fetchone()
    
    cursor.close()
    assert company_count == 1

def test_add_company_noname():
    payload = {
        "company_name": "" #empty name
    }
    company = payload["company_name"]

    add_company_noname_res = requests.post(ENDPOINT + "/company", json=payload)
    
    # Assert that the response status code is 400 (Missing company name)
    assert add_company_noname_res.status_code == 400

    # Assert that the company was successfully added to the database
    assert add_company_noname_res.json()["error"] == "Company name is required."


def test_add_permission_group():
    payload = {
        "permission_group_name": f"Admin_{shortuuid.uuid()}",  # random name of the permission group
        "permission_name": "Add Users, Edit Users, Delete Users, View Users",
        "access_level": "Add, Edit, Delete, View"
    }
    permission_group = payload["permission_group_name"]

    add_group_res = requests.post(ENDPOINT + "/permission-group", json=payload)
    conn.commit()
    # Assert that the response status code is 201 (Created)
    assert add_group_res.status_code == 201

    # Assert that the group was successfully added to the database
    assert add_group_res.json()["message"] == "Permission group added successfully."

    # Assert that the group is now in database
    cursor = conn.cursor()
    cursor.execute("SELECT PermissionGroupName FROM PermissionGroups WHERE PermissionGroupName = %s", (permission_group,))
    group = cursor.fetchone()
    
    cursor.close()
    assert group

def test_add_permission_group_existing():
    pass

def test_add_permission_group_noname():
    pass

def test_add_user():
    pass

def test_add_user_existing():
    pass

def test_add_user_noname():
    pass

def test_add_user_wrong_group():
    pass

def test_add_user_wrong_company():
    pass

def test_edit_user():
    pass

def test_edit_user_wrong_user():
    pass

def test_edit_user_wrong_group():
    pass

def test_list_users():
    pass

def test_list_user_wrong_page():
    pass