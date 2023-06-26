import mysql.connector
from config import USER, PASSWORD, HOST

# Establish a connection to the MySQL server
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD
)

# Create a new database
database_name = "task_colorifix"
create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
conn.cursor().execute(create_database_query)
conn.database = database_name

# Create the Companies table
create_companies_table_query = """
CREATE TABLE IF NOT EXISTS Companies (
    CompanyName VARCHAR(255) NOT NULL PRIMARY KEY
)
"""
conn.cursor().execute(create_companies_table_query)

# Create the PermissionGroups table
create_permission_groups_table_query = """
CREATE TABLE IF NOT EXISTS PermissionGroups (
    PermissionGroupName VARCHAR(255) NOT NULL PRIMARY KEY,
    PermissionNameDescription VARCHAR(255),
    AccessLevelName VARCHAR(255)
)
"""
conn.cursor().execute(create_permission_groups_table_query)

# Create the Users table
create_users_table_query = """
CREATE TABLE IF NOT EXISTS Users (
    UserName VARCHAR(255) NOT NULL PRIMARY KEY,
    PermissionGroupName VARCHAR(255),
    CompanyName VARCHAR(255),
    FOREIGN KEY (PermissionGroupName) REFERENCES PermissionGroups(PermissionGroupName),
    FOREIGN KEY (CompanyName) REFERENCES Companies(CompanyName)
)
"""
conn.cursor().execute(create_users_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
