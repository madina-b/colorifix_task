# Flask API with MySQL Database

This is a Flask API application with a MySQL database backend. It provides endpoints to manage companies, permission groups, and users.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/madina-b/colorifix_task.git
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the MySQL database:
  * Make sure you have MySQL installed and running [[link](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)]
  * Create a new database.
  * Update the database connection details in the config.py file.

4. Run the database initialization script:
   ```bash
   python build_db.py
   ```
## Running the Application
To start the Flask API, run the following command:

```bash
python app.py
```
The API will be accessible at http://localhost:5000.

## Endpoints
1. ### Add a Company
* Endpoint: `POST /companies`
* Request Body (JSON):
  - company_name (string): The name of the company
* Response:
  - Status: 201 (Created) if successful. JSON response with the message "Company added successfully."
  - Status: 400 (Missing company name). JSON response with the "error": "Company name is required."
  - Status: 409 (Company already exists). JSON response with the "error": "Company already exists."

2. ### Add a Permission Group
* Endpoint: `POST /permission-group`
* Request Body (JSON):
  - permission_group_name (string): The name of the permission group
  - permission_name (string): The permission name description
  - access_level (string): Access level
* Response:
  - Status: 201 (Created) if successful. JSON response with the message "Company added successfully."
  - Status: 400 (Missing permission group name or permission name description). JSON response with the "error": "Permission group name and permission name are required."
  - Status: 409 (Permission group already exists). JSON response with the "error": "Cannot add the Permission Group. Permission Group already exists."
 
3. ### Add a User
* Endpoint: `POST /user`
* Request Body (JSON):
  - username (string): The name of the user
  - company_name (string): The name of the company
  - permission_group_name (string): The name of the permission group
* Response:
  - Status: 201 (Created) if successful. JSON response with the message "User added successfully."
  - Status: 400 (Invalid input). JSON response with the "error": "Username, company name, and permission group name are required."
  - Status: 400 (invalid input). JSON response with the "error": "Invalid email address"
  - Status: 409 (User already exists). JSON response with the "error": "User already exists."

4. ### Edit a User
* Endpoint: `PUT /user/<username>`
* Request Body (JSON):
  - username (string): The name of the user
  - company_name (string): The name of the company
  - permission_group_name (string): The name of the permission group
* Response:
  - Status: 201 (Updated) if successful. JSON response with the message "User updated successfully."
  - Status: 404 (Invalid perm.group). JSON response with the "error": "Permission group does not exist."
  - Status: 404 (invalid user). JSON response with the "error": "User does not exist"
  - Status: 400 (invalid input). JSON response with the "error": "Permission group name is required."
  - Status: 409 (User already exists). JSON response with the "error": "User already exists."

5. ### List Users
* Endpoint: `GET /users`
* Request Body OPTIONAL (JSON):
  - page (int): page number, default=1
  - per_page (int): number of records per page, default=10
  - permission_group_name (string): The name of the permission group
* Response:
  - Status: 200 if successful. JSON response with the message `"users": {user_list: {"username": username,
    "permission_group": perm.group,
    "company": company}}`




















