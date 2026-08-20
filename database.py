import mysql.connector
import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
#  Connect using Railway environment variables
conn = mysql.connector.connect(
    host=os.getenv("MYSQLHOST", "turntable.proxy.rlwy.net"),
    port=int(os.getenv("MYSQLPORT", "56394")),  # default if None
    user=os.getenv("MYSQLUSER", "root"),
    password=os.getenv("MYSQLPASSWORD", "ejFGKCewaRMBrEEJsZQZeimkhqBzEmDZ"),
    database=os.getenv("MYSQLDATABASE", "railway")
)

print(" Connected successfully!")

adhar = 0
cursor = conn.cursor()


def ensure_connection():
    global conn, cursor
    try:
        conn.ping(reconnect=True, attempts=3, delay=2)
    except mysql.connector.Error:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQLHOST", "turntable.proxy.rlwy.net"),
            port=int(os.getenv("MYSQLPORT", "56394")),
            user=os.getenv("MYSQLUSER", "root"),
            password=os.getenv("MYSQLPASSWORD", "ejFGKCewaRMBrEEJsZQZeimkhqBzEmDZ"),
            database=os.getenv("MYSQLDATABASE", "railway"),
        )
        cursor = conn.cursor()

def createtable():
    ensure_connection()
    # User table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        adhar_card_no BIGINT PRIMARY KEY,   
        name VARCHAR(100),
        age INT,
        email VARCHAR(100) UNIQUE,
        phno VARCHAR(15)                    
    )
    """)

    # History table with foreign key
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        history_id INT AUTO_INCREMENT PRIMARY KEY,
        adhar_card_no BIGINT,
        question VARCHAR(255),
        respond VARCHAR(255),
        time DATETIME,
        FOREIGN KEY (adhar_card_no) REFERENCES user(adhar_card_no)
    )
    """)

    print(" Tables created successfully!")

# Call the function


def insert():
    ensure_connection()
    adhar_card_no = st.number_input("adhar_card_no")
    name  = st.text_input("name")
    age = st.number_input("age")
    email = st.text_input("email")
    phno = st.number_input("phno")
    
    sql = "INSERT INTO user (adhar_card_no, name, age, email, phno) VALUES (%s,%s,%s,%s,%s)"
    values = (adhar_card_no,name,age,email,phno)
    
    cursor.execute(sql,values)
    conn.commit()
    print("user insearted sucessfully")
    adhar = adhar_card_no
    return adhar_card_no

def activity(question,respond,adhar_no):
    ensure_connection()
    time = datetime.now()
    sql = "INSERT INTO history (adhar_card_no, question, respond, time) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql, (adhar_no, question, respond, time))
    conn.commit()


def authenticate(adhar_card_no, email):
    ensure_connection()
    cursor.execute(
        "SELECT adhar_card_no FROM user WHERE adhar_card_no = %s AND email = %s",
        (adhar_card_no, email),
    )
    return cursor.fetchone() is not None


def create_user(adhar_card_no, name, age, email, phno):
    ensure_connection()
    cursor.execute(
        "INSERT INTO user (adhar_card_no, name, age, email, phno) VALUES (%s,%s,%s,%s,%s)",
        (adhar_card_no, name, age, email, phno),
    )
    conn.commit()


def get_history(adhar_card_no):
    ensure_connection()
    cursor.execute(
        "SELECT question, respond, time FROM history WHERE adhar_card_no = %s ORDER BY time DESC",
        (adhar_card_no,),
    )
    return cursor.fetchall()


createtable()

