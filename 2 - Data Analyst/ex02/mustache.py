import psycopg
import matplotlib.pyplot as plt

query = """
            SELECT
                SUM(price) AS total,
                ROUND(AVG(price), 2) AS mean,
                ROUND(STDDEV(price), 2) AS std,
                MIN(price) AS min,
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS q1,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS q2,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS q3,
                MAX(price) AS max
            FROM customers
            WHERE event_type = 'purchase'
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
    cur.execute("SELECT price FROM customers WHERE event_type = 'purchase'")
    prices = cur.fetchall()

(total, mean, std, min_price, q1, q2, q3, max_price) = data[0]

print(f"count   {total:.6f}")
print(f"mean {mean:.6f}")
print(f"std  {std:.6f}")
print(f"min  {min_price:.6f}")
print(f"25%  {q1:.6f}")
print(f"50%  {q2:.6f}")
print(f"75%  {q3:.6f}")
print(f"max  {max_price:.6f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
boxes = ax1.boxplot(prices,
                    vert=False,
                    widths=0.5,
                    notch=True,
                    boxprops=dict(
                        facecolor='lightgray',
                        edgecolor='none'
                    ),
                    flierprops=dict(
                        marker='D',
                        markersize=8,
                        markerfacecolor='lightgray',
                        markeredgecolor='none'
                    ),
                    patch_artist=True)
ax1.set_yticks([])
ax1.set_xlabel("Price")
ax1.set_title("Full Box Plot")

boxprops = dict(facecolor='green', edgecolor='black')
medianprops = dict(linestyle='-', linewidth=2, color='black')

ax2.boxplot(prices,
            vert=False,
            widths=0.5,
            notch=True,
            boxprops=boxprops,
            medianprops=medianprops,
            showfliers=False,
            patch_artist=True)

ax2.set_yticks([])
ax2.set_xlabel("Price")
ax2.set_title("Interquartile range (IQR)")

plt.tight_layout()
plt.show()

conn.close()
