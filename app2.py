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
        return 'Hello, World!'
    
    @app.route('/search/<q>')
    def phyla(q):
        
        
        return phyla_input, 'Hello, Phyla World!'
    
    
if __name__ == '__main__':
    app.run()

main()