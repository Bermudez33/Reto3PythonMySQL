import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database= "digital_nao_reto_3"
)

if connection.is_connected():
    print('Connected Succesfully')
else:
    print('Failed to connect')

connection.close()