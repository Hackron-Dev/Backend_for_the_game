import psycopg2

con = psycopg2.connect(
    database="forgame",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = con.cursor()
