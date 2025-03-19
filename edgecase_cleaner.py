import psycopg2 as psy

def clean_family(cur):
    cur.execute("UPDATE species SET family_id = (SELECT family_id FROM family WHERE family = 'valerianaceae') WHERE family_id = (SELECT family_id FROM family WHERE family = 'vvalerianaceae');")
    cur.execute("DELETE FROM family WHERE family = 'vvalerianaceae';")
    cur.execute("UPDATE species SET family_id = (SELECT family_id FROM family WHERE family = 'verbenaceae') WHERE family_id IN (SELECT family_id FROM family WHERE family LIKE '%verbenaceae');")
    cur.execute("UPDATE genera SET family_id = (SELECT family_id FROM family WHERE family = 'verbenaceae') WHERE family_id IN (SELECT family_id FROM family WHERE family IN ('‘verbenaceae', 'vverbenaceae', '‘vverbenaceae'));")
    cur.execute("DELETE FROM family WHERE family IN ('‘verbenaceae', 'vverbenaceae', '‘vverbenaceae');")
    cur.execute("UPDATE family SET family = 'hemerocallidaceae' WHERE family = 'emerocallidaceae';")
    cur.execute("UPDATE species SET family_id = (SELECT family_id FROM family WHERE family = 'menyanthaceae') WHERE family_id = (SELECT family_id FROM family WHERE family = 'enyanthaceae');")
    cur.execute("UPDATE genera SET family_id = (SELECT family_id FROM family WHERE family = 'menyanthaceae') WHERE family_id = (SELECT family_id FROM family WHERE family = 'enyanthaceae');")
    cur.execute("DELETE FROM family WHERE family = 'enyanthaceae';")
    cur.execute("UPDATE species SET family_id = (SELECT family_id FROM family WHERE family = 'hamamelidaceae') WHERE family_id = (SELECT family_id FROM family WHERE family LIKE '');")
    cur.execute("DELETE FROM family WHERE family LIKE '';")
    return

def clean_genera(cur):
    cur.execute("UPDATE genera SET genera = 'ilex' WHERE genera = 'tlex';")
    cur.execute("UPDATE genera SET genera = 'ionactis' WHERE genera = 'tonactis';")
    cur.execute("UPDATE species SET genera_id = (SELECT genera_id FROM genera WHERE genera = 'iris') WHERE genera_id = (SELECT genera_id FROM genera WHERE genera = 'tris');")
    cur.execute("DELETE FROM genera WHERE genera = 'tris';")
    cur.execute("UPDATE genera SET genera = 'buchloë' WHERE genera = 'buchloë';")
    cur.execute("UPDATE species SET genera_id = (SELECT genera_id FROM genera WHERE genera = 'symphyotrichum') WHERE genera_id = (SELECT genera_id FROM genera WHERE genera = 'symphy');")
    cur.execute("DELETE FROM genera WHERE genera = 'symphy';")
    cur.execute("UPDATE genera SET genera = 'iodanthus' WHERE genera = 'todanthus';")
    cur.execute("UPDATE species SET genera_id = (SELECT genera_id FROM genera WHERE genera = 'hamamelis') WHERE genera_id = (SELECT genera_id FROM genera WHERE genera LIKE 'hamamelidaceae%');")
    cur.execute("DELETE FROM genera WHERE genera LIKE 'hamamelidaceae%';")
    cur.execute("UPDATE species SET genera_id = (SELECT genera_id FROM genera WHERE genera = 'ulmus') WHERE genera_id = (SELECT genera_id FROM genera WHERE genera = 'ulnus');")
    cur.execute("DELETE FROM genera WHERE genera = 'ulnus';")
    return

def clean_species(cur):
    cur.execute("UPDATE species SET scientific_name = 'hamamelis vernalis sarg.' WHERE scientific_name = 'hamamelidaceaehamamelis vernalis sarg.';")
    cur.execute("UPDATE species SET common_name = REPLACE(common_name, 'fem', 'fern') WHERE common_name LIKE '%\\fem';")
    cur.execute("UPDATE species SET common_name = REPLACE(common_name, 'tice', 'rice') WHERE common_name LIKE 'tice';")
    cur.execute("UPDATE species SET common_name = REPLACE(common_name, 'shepherd’ s-purse', 'shepherd’s-purse') WHERE common_name LIKE 'shepherd’ s-purse';")
    return

def main():
    
    conn = psy.connect('dbname=plant-container user=postgres password=password host=0.0.0.0 port=30420')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SET search_path TO ar_plants;")
    
    clean_genera(cur)

    clean_family(cur)
    cur.close
    
    clean_species(cur)
    return


main()