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

for row in rows:
  ids.append(row[0])
  textos.append(row[1])
  usuarios.append(row[2])
  hashtags.append(row[3])
  fechas.append(row[4])
  retweets.append(row[5])
  favoritos.append(row[6])
  

offset += batch_size
print(f"Done {offset}")
palabras_limpias = []
palabras_eliminar = ['elpaiscomuy', 'elobservadorcomuy']

nombres_usuarios = set(usuarios)


for texto_tweet in textos:
    texto_limpio = re.sub(r'http\S+', '', texto_tweet)
    palabras_tokenizadas = word_tokenize(texto_limpio.lower())
    palabras_tokenizadas = [re.sub(r'[^\w\s]', '', palabra) for palabra in palabras_tokenizadas if len(palabra) > 0]
    palabras_limpias.extend([palabra for palabra in palabras_tokenizadas if palabra and palabra not in stop_words and not any(palabra.startswith(usuario) for usuario in nombres_usuarios) and not any(palabra.startswith(palabra_eliminar) for palabra_eliminar in palabras_eliminar)])
    
conteo_palabras = Counter(palabras_limpias)
top_palabras = conteo_palabras.most_common(5)

print(top_palabras)

mycursor.close()
mydb.close()

palabras_top = [palabra for palabra, frecuencia in top_palabras]
frecuencias_top = [frecuencia for palabra, frecuencia in top_palabras]


plt.figure(figsize=(10, 6))
plt.bar(palabras_top, frecuencias_top, color=["#4C2A85", "#BE96FF", "#957DAD"])
plt.xlabel('Palabras')
plt.ylabel('Frecuencia')
plt.title('Top 5 Palabras Más Frecuentes')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


print("Done")
