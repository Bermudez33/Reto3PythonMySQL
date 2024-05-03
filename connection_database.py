import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database= "sys",
  port=""
)

mycursor = mydb.cursor()

with open('C:\\Users\\dxber\\Downloads\\tweets_extraction.json','r') as file:
    data = json.load(file)
    # print(reader)
    for item in data:
          mycursor.execute("""
                          INSERT IGNORE INTO tweets (id, texto, usuario, hashtags, fecha, retweets, favoritos)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                          """, (item['id'], item['texto'], item['usuario'], json.dumps(item['hashtags']), item['fecha'], item['retweets'], item['favoritos']))
                                                                            
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

