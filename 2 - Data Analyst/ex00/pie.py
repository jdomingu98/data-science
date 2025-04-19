from dotenv import load_dotenv
import os
import psycopg
import matplotlib.pyplot as plt

load_dotenv()

dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")


with open("pie.sql", "r") as file:
    query = file.read()

conn = psycopg.connect(
    dbname=dbname,
    user=user,
    password=password,
    host="localhost"
)

with conn.cursor() as cur:
    cur.execute(query)
    data = cur.fetchall()

labels = [row[0] for row in data]
amount = [row[1] for row in data]

plt.pie(amount, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Event Type Distribution')
plt.axis('equal')  # Equal ensures that pie is drawn as a circle.
plt.show()

conn.close()
