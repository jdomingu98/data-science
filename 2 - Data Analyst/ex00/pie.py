import psycopg
import matplotlib.pyplot as plt

query = """
            SELECT event_type AS element, COUNT(*) AS recording
            FROM customers
                GROUP BY event_type;
        """

conn = psycopg.connect(
    dbname='piscineds',
    user='jdomingu',
    password='mysecretpassword',
    host='localhost',
    port='5433',
)

with conn.cursor() as cur:
    cur.execute(query)
    data = cur.fetchall()

labels = [row[0] for row in data]
amount = [row[1] for row in data]

plt.pie(amount, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Event Type Distribution')
plt.axis('equal')  # Ensures is drawn as a circle
plt.show()

conn.close()
