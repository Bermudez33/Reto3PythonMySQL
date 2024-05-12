import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import matplotlib.pyplot as plt
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))

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

total_usuarios = {}
total_retweets = {}
palabras_limpias = []
palabras_eliminar = ['elpaiscomuy', 'elobservadorcomuy']
nombres_usuarios = set(usuarios)

for row in rows:
  ids.append(row[0])
  textos.append(row[1])
  usuarios = row[2]
  hashtags.append(row[3])
  fechas.append(row[4])
  retweets.append(row[5])
  favoritos.append(row[6])
  total_usuarios[usuarios] = total_usuarios.get(usuarios, 0) + 1
  total_retweets[row[2]] = total_retweets.get(row[2], 0) + row[5]

offset += batch_size
print(f"Done {offset}")

for texto_tweet in textos:
    texto_limpio = re.sub(r'http\S+', '', texto_tweet)
    palabras_tokenizadas = word_tokenize(texto_limpio.lower())
    palabras_tokenizadas = [re.sub(r'[^\w\s]', '', palabra) for palabra in palabras_tokenizadas if len(palabra) > 0]
    palabras_limpias.extend([palabra for palabra in palabras_tokenizadas if palabra and palabra not in stop_words 
                             and not any(palabra.startswith(usuario) for usuario in nombres_usuarios)
                              and not any(palabra.startswith(palabra_eliminar) for palabra_eliminar in palabras_eliminar)])

conteo_palabras = Counter(palabras_limpias)
top_palabras = conteo_palabras.most_common(5)

print(top_palabras)

mycursor.close()
mydb.close()

sorted_usuarios = dict(sorted(total_usuarios.items(), key=lambda x: x[1], reverse=True))
top_users = dict(list(sorted_usuarios.items())[:5])

sorted_retweets = dict(sorted(total_retweets.items(), key=lambda x: x[1], reverse=True))
top_users_retweets = dict(list(sorted_retweets.items())[:5])

palabras_top = [palabra for palabra, frecuencia in top_palabras]
frecuencias_top = [frecuencia for palabra, frecuencia in top_palabras]

fig1, ax1 = plt.subplots()
ax1.bar(top_users.keys(), top_users.values(), color=["#4C2A85", "#BE96FF", "#957DAD"])
ax1.set_title("Top 5 Usuarios con más Tweets")
ax1.set_xlabel("Usuarios")
ax1.set_ylabel("Total Tweets")
ax1.set_xticklabels(top_users.keys(), rotation=0)
plt.tight_layout()

fig2, ax2 = plt.subplots()
ax2.pie(top_users_retweets.values(), labels=top_users_retweets.keys(), autopct='%1.1f%%', startangle=140)
ax2.set_title("Top 5 Usuarios con más Retweets")
ax2.axis('equal')  
plt.tight_layout()

fig3, ax3 = plt.subplots()
plt.bar(palabras_top, frecuencias_top, color=["#4C2A85", "#BE96FF", "#957DAD"])
ax3.set_xlabel('Palabras')
ax3.set_ylabel('Frecuencia')
ax3.set_title('Top 5 Palabras Más Frecuentes')
ax3.set_xticklabels(rotation=0)
plt.tight_layout()

print("Done")

root = tk.Tk()
root.title("Dashboard")
root.state('zoomed')

upper_frame = tk.Frame(root)
upper_frame.pack(fill="both", expand=True)

canvas1 = FigureCanvasTkAgg(fig1, upper_frame)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left",fill="both",expand=True)

canvas2 = FigureCanvasTkAgg(fig2, upper_frame)
canvas2.draw()
canvas2.get_tk_widget().pack(side="left",fill="both",expand=True)

canvas3 = FigureCanvasTkAgg(fig3, upper_frame)
canvas3.draw()
canvas3.get_tk_widget().pack(side="left",fill="both",expand=True)

root.mainloop()
