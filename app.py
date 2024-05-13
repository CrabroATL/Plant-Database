import psycopg2

def main():
    

    # load in the plant database
    
    print("cool")
    conn = psycopg2.connect('dbname=plants user=postgres password=password host=host.docker.internal')
    print("more cool")

    print("test")
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

    