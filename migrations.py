import psycopg2 as psy

conn = psy.connect('dbname=postgres user=postgres password=password host=0.0.0.0 port=30420')
cur = conn.cursor()
conn.autocommit = True
migration = open("migrations/plants.pgsql", "r")
pgsql = migration.read()
cur.execute(pgsql)

conn.close




