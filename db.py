import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234"
    )

def init_db():
    conn = create_connection()
    cursor = conn.cursor()

    # FIXED NAME
    cursor.execute("CREATE DATABASE IF NOT EXISTS crime")
    cursor.execute("USE crime")

    # UPDATED TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registration (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fullname VARCHAR(100),
        username VARCHAR(50) UNIQUE,
        email VARCHAR(100) UNIQUE,
        phone VARCHAR(15),
        gender VARCHAR(10),
        password VARCHAR(100)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        state VARCHAR(100),
        year INT,
        predicted_crime INT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES registration(id)
    )
    """)

    conn.commit()
    conn.close()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="crime"
        
    )