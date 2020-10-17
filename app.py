import streamlit as st
import pandas as pd
import numpy as np
import string
import requests
import sqlite3
import json
conn = sqlite3.connect('data.db')
c = conn.cursor()
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
def create_spamtable():
    c.execute('CREATE TABLE IF NOT EXISTS spamtable(username TEXT,spam INTEGER)')
def create_hamtable():
    c.execute('CREATE TABLE IF NOT EXISTS hamtable(username TEXT,message TEXT,ham INTEGER)')
def add_spamdata(username,spam):
	c.execute('INSERT INTO spamtable(username,spam) VALUES (?,?)',(username,spam))
	conn.commit()
def add_hamdata(username,message,ham):
	c.execute('INSERT INTO hamtable(username,message,ham) VALUES (?,?,?)',(username,message,ham))
	conn.commit()
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def view_all_spam():
	c.execute('SELECT * FROM spamtable')
	data = c.fetchall()
	return data
def view_all_ham():
	c.execute('SELECT * FROM hamtable')
	data = c.fetchall()
	return data
def main():
    st.title("Built By Gautam Jain")
    html_temp = """
               <div style="background-color:#00FF00 ;padding:10px">
               <h1 style="color:white;text-align:center;">Lyrics Generator app</h1>
               </div>
               """
    st.markdown(html_temp, unsafe_allow_html=True)
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        st.info("This Is a Email Detection Model Used to Detect Whether A Mail Recieved By The User Is Spam Or Ham.")
        st.success("You Need To Sign Up to Access The Model")
    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                st.markdown("Fill Your Information Here")
                artist = st.text_input("Singer Name")
                song = st.text_input("Title")
                st.warning('Click Here To Check Your Results')
                if st.button("click here"):
                    url = "http://api.lyrics.ovh/v1/" + artist + '/' + song
                    response = requests.get(url)
                    json_data = json.loads(response.content)
                    lyrics = json_data['lyrics']
                    st.text("{}".format(lyrics))
            else:
                st.warning("Incorrect Username/Password")
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        st.selectbox("Your Gender", ["Male", "Female", "Others"])
        Age=st.text_input("Age")


        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to Login Your Account")

if __name__=="__main__":
    main()