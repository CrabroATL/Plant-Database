from flask import Flask, request, jsonify, redirect, render_template, request
import psycopg2

app = Flask(__name__)


def main():

    # load in the plant database
    

    conn = psycopg2.connect('dbname=postgres user=postgres password=password host=host.docker.internal')

    cur = conn.cursor()
    
    # page skeletons

    @app.route('/')
    def home():
        print("home")
        return render_template('index.html')
    
    @app.route('/search')
    def search():
        phyla = request.args.get("phyla")
        family = request.args.get("family")
        print(family)
        print(phyla)
        cur.execute("SET search_path TO ar_plants;")
        if phyla is not None:
            cur.execute("SELECT phyla_id FROM phyla WHERE polyphylactic_group = (%s);", (phyla,))
            phyla_id = cur.fetchone()
            phyla_id = phyla_id[0]
            cur.close
            print(phyla_id)
        if family is not None and phyla is not None:
            cur.execute("SELECT family FROM family WHERE family_id = (SELECT family_id FROM family WHERE family LIKE '(%s)%' AND phyla_id = (%s));", (family, phyla_id,))
            family = cur.fetchall()
            cur.close
        print(phyla_id)
        print(family)
        
        return render_template('results.html', phyla = phyla, family = family)

    @app.route('/phyla')
    def phyla():
        phyla_input = request.form.get("phyla")
        
        return phyla_input, 'Hello, Phyla World!'
    
    @app.route('/family')
    def family():
        return 'Hello, Family World!'
    
    @app.route('/genera')
    def route():
        return 'Hello, Genera World!'

    @app.route('/species')
    def species():
        return 'Hello, Species World!'
    
    @app.route('/county')
    def county():
        return 'Hello, County World!'
    
    @app.route('/results')
    def results():
        return 'Hello, Results Worlds!'
    # API skeletons

    @app.route('/phyla/<phyla_id>')
    def get_phyla(phyla_id):
        
        phyla_id = 1
        cur.execute("SELECT polyphylactic_group FROM ar_plants.phyla WHERE phyla_id = (%s)", (phyla_id,))
        phyla = cur.fetchone()
        print(phyla)
        cur.close()
        return phyla
    
    @app.route('/family/<family_id>')
    def get_family(family_id):
        family_id = 1
        cur.execute("SELECT family FROM ar_plants.family WHERE family_id = (%s)", (family_id,))
        family = cur.fetchone()
        print(family)
        cur.close()
        return family
    
    @app.route('/genera/<genera_id>')
    def get_genera(genera_id):
        genera_id = 1
        cur.execute("SELECT genera FROM ar_plants.genera WHERE genera_id = (%s)", (genera_id,))
        genera = cur.fetchone()
        print(genera)
        cur.close()
        return genera
    
    @app.route('/species/<species_id>')
    def get_species(species_id):
        species_id = 1
        cur.execute("SELECT species FROM ar_plants.species WHERE genera_id = (%s)", (species_id,))
        species = cur.fetchone()
        print(species)
        cur.close()
        return species



main()