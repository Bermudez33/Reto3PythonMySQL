import mysql.connector
import json
from datetime import datetime


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database= "sys",
  port="3307"
)

mycursor = mydb.cursor()

with open('C:\\Users\\dxber\\Downloads\\tweets_extraction.json','r') as file:
    data = json.load(file)
    # print(reader)
    for item in data:
          
          fecha = datetime.strptime(item['fecha'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")

          mycursor.execute("""
                          INSERT IGNORE INTO tweets (id, texto, usuario, hashtags, fecha, retweets, favoritos)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                          """, (item['id'], item['texto'], item['usuario'], json.dumps(item['hashtags']), fecha, item['retweets'], item['favoritos']))
                                                                            
          print(mycursor.rowcount, "row got inserted")
    mydb.commit()
    

mycursor.close()
mydb.close()

print("Done")


# sql = 'INSERT INTO tweets (id, texto, usuario, hashtags, fecha, retweets, favoritos) VALUES (%s,%s,%s,%s,%s,%s,%s)'




# mycursor.execute('SELECT * FROM tweets;')

# myresult = mycursor.fetchall()

# for x in myresult:
#   print(x)

# if connection.is_connected():
#     print('Connected Succesfully')
# else:
#     print('Failed to connect')

