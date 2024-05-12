import mysql.connector
import matplotlib.pyplot as plt

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootPassword123",
  database= "sys",
  port="3307"
)

mycursor = mydb.cursor()

batch_size = 289329
offset = 0

ids = []
textos = []
usuarios = []
hashtags = []
fechas = []
retweets = []
favoritos = []

mycursor.execute("SELECT id,texto,usuario,hashtags,fecha,retweets,favoritos FROM tweets LIMIT %s", (batch_size,))

rows = mycursor.fetchall()

total_retweets = {}

for row in rows:
  ids.append(row[0])
  textos.append(row[1])
  usuarios = row[2]
  hashtags.append(row[3])
  fechas.append(row[4])
  retweets.append(row[5])
  favoritos.append(row[6])
  total_retweets[row[2]] = total_retweets.get(row[2], 0) + row[5]

offset += batch_size
print(f"Done {offset}")

  

mycursor.close()
mydb.close()

sorted_retweets = dict(sorted(total_retweets.items(), key=lambda x: x[1], reverse=True))
top_users_retweets = dict(list(sorted_retweets.items())[:5])


plt.figure(figsize=(8, 8))
plt.pie(top_users_retweets.values(), labels=top_users_retweets.keys(), autopct='%1.1f%%', startangle=140)
plt.title("Top 5 Usuarios con más Retweets")
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.tight_layout()
plt.show()


print("Done")
