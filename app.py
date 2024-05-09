import psycopg2
import traceback

def main():
    print("working")

    # load in the plant database
    try:
        conn = psycopg2.connect('dbname=plants user=postgres password=password host=0.0.0.0')

    except psycopg2.Error as e:
        print (e)
        print (e.pgcode)
        print (e.pgerror)
        print (traceback.format_exc())
        exit(0)

    cur = conn.cursor()

    phyla = cur.execute("SELECT * FROM stuff.fruit")
    print(phyla)
    cur.close()

    print(phyla)
    print("victory")
    conn.close()
    


    # accept user input to search the database

    # select data from database

    # return data to user
    
main()

    