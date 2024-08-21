import psycopg2 as psy

def clean_family(cur):
    cur.execute("UPDATE species SET family_id = (SELECT family_id FROM family WHERE family = 'VALERIANACEAE') WHERE family_id = (SELECT family_id FROM family WHERE family = 'VVALERIANACEAE');")
    cur.execute("DELETE FROM family WHERE family = 'VVALERIANACEAE';")
    cur.execute("UPDATE species SET family_id = (SELECT family_id FROM family WHERE family = 'VERBENACEAE') WHERE family_id IN (SELECT family_id FROM family WHERE family LIKE '%VERBENACEAE');")
    cur.execute("UPDATE genera SET family_id = (SELECT family_id FROM family WHERE family = 'VERBENACEAE') WHERE family_id IN (SELECT family_id FROM family WHERE family IN ('‘VERBENACEAE', 'VVERBENACEAE', '‘VVERBENACEAE'));")
    cur.execute("DELETE FROM family WHERE family IN ('‘VERBENACEAE', 'VVERBENACEAE', '‘VVERBENACEAE');")
    cur.execute("UPDATE family SET family = 'HEMEROCALLIDACEAE' WHERE family = 'EMEROCALLIDACEAE';")
    cur.execute("UPDATE species SET family_id = (SELECT family_id FROM family WHERE family = 'MENYANTHACEAE') WHERE family_id = (SELECT family_id FROM family WHERE family = 'ENYANTHACEAE');")
    cur.execute("UPDATE genera SET family_id = (SELECT family_id FROM family WHERE family = 'MENYANTHACEAE') WHERE family_id = (SELECT family_id FROM family WHERE family = 'ENYANTHACEAE');")
    cur.execute("DELETE FROM family WHERE family = 'ENYANTHACEAE';")
    cur.execute("UPDATE species SET family_id = (SELECT family_id FROM family WHERE family = 'HAMAMELIDACEAE') WHERE family_id = (SELECT family_id FROM family WHERE family LIKE '');")
    cur.execute("DELETE FROM family WHERE family LIKE '';")
    return

def clean_genera(cur):
    cur.execute("UPDATE genera SET genera = 'Ilex' WHERE genera = 'Tlex';")
    cur.execute("UPDATE genera SET genera = 'Ionactis' WHERE genera = 'Tonactis';")
    cur.execute("UPDATE species SET genera_id = (SELECT genera_id FROM genera WHERE genera = 'Iris') WHERE genera_id = (SELECT genera_id FROM genera WHERE genera = 'Tris');")
    cur.execute("DELETE FROM genera WHERE genera = 'Tris';")
    cur.execute("UPDATE genera SET genera = 'Buchloë' WHERE genera = 'Buchloé'")
    cur.execute("UPDATE species SET genera_id = (SELECT genera_id FROM genera WHERE genera = 'Symphyotrichum') WHERE genera_id = (SELECT genera_id FROM genera WHERE genera = 'Symphy');")
    cur.execute("DELETE FROM genera WHERE genera = 'Symphy';")
    cur.execute("UPDATE genera SET genera = 'Iodanthus' WHERE genera = 'Todanthus';")
    cur.execute("UPDATE species SET genera_id = (SELECT genera_id FROM genera WHERE genera = 'Hamamelis') WHERE genera_id = (SELECT genera_id FROM genera WHERE genera LIKE 'HAMAMELIDACEAE%');")
    cur.execute("DELETE FROM genera WHERE genera LIKE 'HAMAMELIDACEAE%'") 
    cur.execute("UPDATE species SET genera_id = (SELECT genera_id FROM genera WHERE genera = 'Ulmus') WHERE genera_id = (SELECT genera_id FROM genera WHERE genera = 'Ulnus');")
    cur.execute("DELETE FROM genera WHERE genera = 'Ulnus';")
    return

def clean_species(cur):
    cur.execute("UPDATE species SET scientific_name = 'Hamamelis vernalis Sarg.' WHERE scientific_name = 'HAMAMELIDACEAEHamamelis vernalis Sarg.'")
    cur.execute("UPDATE species SET common_name = REPLACE(common_name, 'fem', 'fern') WHERE common_name LIKE '%\\fem'")
    cur.execute("UPDATE species SET common_name = REPLACE(common_name, 'tice', 'rice') WHERE common_name LIKE 'tice'")
    return




def main():
    
    conn = psy.connect('dbname=postgres user=postgres password=password host=0.0.0.0 port=30420')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SET search_path TO ar_plants;")
    

    clean_genera(cur)

    clean_family(cur)
    cur.close
    
    clean_species(cur)
    return


main()