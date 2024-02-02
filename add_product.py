import pygame
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost', 
    user='root',
    password='maysa1995',
    database='store'
)

mycursor = mydb.cursor()


    