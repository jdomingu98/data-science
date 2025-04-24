import math
import matplotlib.pyplot as plt
import numpy as np
import psycopg

from matplotlib.ticker import FuncFormatter

query1 = """
            SELECT DATE(event_time) AS event_date, COUNT(*) AS purchase_count
            FROM customers
                WHERE event_type = 'purchase' AND (
                    EXTRACT(MONTH FROM event_time) >= 10 OR
                    EXTRACT(MONTH FROM event_time) <= 1
                )
                GROUP BY DATE(event_time)
                ORDER BY event_date;
        """

query2 = """
            SELECT TO_CHAR(event_time, 'Mon') AS month,
                SUM(price) * 0.8 AS amount
            FROM customers
                WHERE event_type = 'purchase' AND (
                    EXTRACT(MONTH FROM event_time) >= 10 OR
                    EXTRACT(MONTH FROM event_time) <= 1
                )
                GROUP BY TO_CHAR(event_time, 'Mon'),
                    EXTRACT(MONTH FROM event_time)
                ORDER BY EXTRACT(MONTH FROM event_time) DESC;
        """

query3 = """
            SELECT DATE_TRUNC('day', event_time) AS day_date,
                ROUND(
                    SUM(price) / NULLIF(COUNT(DISTINCT user_id), 0),
                2) AS amount
            FROM customers
                WHERE event_type = 'purchase' AND (
                    EXTRACT(MONTH FROM event_time) >= 10 OR
                    EXTRACT(MONTH FROM event_time) <= 1
                )
                GROUP BY DATE_TRUNC('day', event_time)
                ORDER BY DATE_TRUNC('day', event_time);
        """

conn = psycopg.connect(
    dbname='piscineds',
    user='jdomingu',
    password='mysecretpassword',
    host='localhost',
    port='5433',
)

labels_x = ["Oct", "Nov", "Dec", "Jan"]


def get_quartiles(dates):
    """
    This function calculates the quartiles of a list of dates.
    It returns a list of indices that correspond to the quartiles.
    """
    return [0,
            len(dates) // 4,
            len(dates) // 2,
            3 * len(dates) // 4]


def chart1(query):
    """
    This function creates a line chart showing the number of purchases made by
    customers over the months of October, November, December, and January.
    """

    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()

    dates, counts = zip(*data)
    quartiles = get_quartiles(dates)

    plt.figure(figsize=(10, 6))
    plt.xticks([dates[i] for i in quartiles], labels_x)
    plt.xlim(dates[0], dates[-1])
    plt.ylabel("Number of customers")
    plt.gca().yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f'{int(x / 10)}')
    )
    plt.plot(dates, counts, linestyle='-')
    plt.show()


def chart2(query):
    """
    This function creates a bar chart showing the total sales made by customers
    over the months of October, November, December, and January.
    """
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()

    dates, counts = zip(*data)
    quartiles = get_quartiles(dates)

    plt.figure(figsize=(10, 6))
    plt.bar(dates, counts)
    plt.xticks([dates[i] for i in quartiles], labels_x)
    plt.xlabel("Month")
    plt.ylabel("Total sales in million of ₳")
    plt.show()


def chart3(query):
    """
    This function creates a line chart showing the average spend per customer
    over the months of October, November, December, and January.
    """
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()

    dates, counts = zip(*data)
    quartiles = get_quartiles(dates)

    plt.figure(figsize=(10, 6))
    plt.xticks([dates[i] for i in quartiles], labels_x)
    plt.xlim(dates[0], dates[-1])
    plt.ylabel("Average spend/customers in ₳")
    plt.ylim(0)
    plt.yticks(np.arange(0, math.ceil(max(counts) / 5) * 5 + 1, 5))
    plt.plot(dates, counts, linestyle='-')
    plt.fill_between(dates, counts)
    plt.show()

    pass


def main():
    """
    This function calls the chart1 function to create the line chart.
    """
    chart1(query1)
    chart2(query2)
    chart3(query3)


if __name__ == "__main__":
    main()
    conn.close()
