import mysql.connector
import matplotlib.pyplot as plt

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
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

total_usuarios = {}

for row in rows:
  ids.append(row[0])
  textos.append(row[1])
  usuarios = row[2]
  hashtags.append(row[3])
  fechas.append(row[4])
  retweets.append(row[5])
  favoritos.append(row[6])
  total_usuarios[usuarios] = total_usuarios.get(usuarios, 0) + 1

offset += batch_size
print(f"Done {offset}")

  

mycursor.close()
mydb.close()

sorted_usuarios = dict(sorted(total_usuarios.items(), key=lambda x: x[1], reverse=True))
top_users = dict(list(sorted_usuarios.items())[:5])

fig1, ax1 = plt.subplots()
ax1.bar(top_users.keys(), top_users.values(), color=["#4C2A85", "#BE96FF", "#957DAD"])
ax1.set_title("Top 5 Usuarios con más Tweets")
ax1.set_xlabel("Usuarios")
ax1.set_ylabel("Total Tweets")
ax1.set_xticklabels(top_users.keys(), rotation=0)
plt.tight_layout()
plt.show()



print("Done")

