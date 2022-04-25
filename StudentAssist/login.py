from flask import Flask
from __init__ import app
import logging
import os
from db_connector import createUser
import click

#def signing_up():
 #when sign up botton is clicked
 
if signing_up == true:
  first = input('First Name: ')
  last = input('Last Name: ')
  phone = input("Phone Number (Optional): ")
  user_email = input("Email: ") 
#check in the email already exist in database.
  for user_email in db:
    while user_email == createUser(emailAddress):
      print("This email is already in use.")
            #create pop up
    user_email = input("Email: ")
#no restrictions on password but must have a password.
  user_password = input("Password: ")
#check password
  while user_password == (' '):
    print('Password must be at least one character long.')
     #create pop up
    user_password = input('Password: ')
  createUser(first, last, user_email, user_password, true, true)
#store email info in database.
    

#gets info that already exist in database(s)
#def login()
 #when a login button is clicked
if login == true:
  user_email = input("Email: ")
  for user_email in createUser(emailAddress):
    while user_email != createUser(emailAddress):
      #might create an infinite loop
      print("This email does not exist, try again.")
      user_email = input("Email: ")
  user_password = input("Password: ")
#compare to password already associated with account
  while user_password != createUser(password):
    print("Incorrect password, try again.")
    user_password = input("Password: ")
#end. enter account home page.

#Not sure how log out word work