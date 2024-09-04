package main

import (
	"context"
	"encoding/json"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/jackc/pgx/v5/pgxpool"
)

func handlerFunc(w http.ResponseWriter, r *http.Request) {
	switch r.URL.Path {
	case "/":
		mainPage(w, r)
	case "/search":
		searchResults(w, r)
	}
}

type county struct {
	Index      int
	CountyName string `json:"counties"`
}

func newCounty(index int, countyName string) county {
	c := county{
		Index:      index,
		CountyName: countyName,
	}
	return c
}

func checkCounties(r *http.Request) []county {
	countiesJson, err := os.Open("counties.json")
	if err != nil {
		fmt.Println(err)
	}
	byteValue, err := io.ReadAll(countiesJson)
	if err != nil {
		fmt.Println(err)
	}
	var j map[string]string
	json.Unmarshal(byteValue, &j)
	r.ParseForm()
	var currentCounties []county
	for counties, name := range r.Form["counties"] {
		c := newCounty(counties, name)
		currentCounties = append(currentCounties, c)
	}
	return currentCounties
}

func searchResults(w http.ResponseWriter, r *http.Request) {
	queryDB(r)

	tmpl := make(map[string]*template.Template)
	tmpl["results.html"] = template.Must(template.ParseFiles("results.html", "layout.html"))
	tmpl["results.html"].ExecuteTemplate(w, "layout", nil)
}

func mainPage(w http.ResponseWriter, r *http.Request) {
	tmpl := make(map[string]*template.Template)
	tmpl["index.html"] = template.Must(template.ParseFiles("index.html", "layout.html"))
	tmpl["index.html"].ExecuteTemplate(w, "layout", nil)
}

func getPlant(phyla string, family string, genera string, commonName string, scientificName string, counties []county) {
	conn, err := pgxpool.New(context.Background(), "postgres://postgres:password@localhost:30420/postgres")
	fmt.Println(err)
	if err != nil {
		log.Fatalf("Unable to connect to database: %v", err)
	}
	defer conn.Close()

	test, errr := conn.Exec(context.Background(), "SET search_path TO ar_plants")
	if err != nil {
		log.Fatal(errr)
	} else {
		fmt.Println("check", test)
	}
}

// getPhyla, err := conn.Query(context.Background(), "SELECT species FROM species WHERE phyla=%s", phyla)
// if err != nil {
// 	fmt.Println(err)
// }
// defer rows.Close()

// families, err := conn.Query(context.Background(), "SELECT species FROM species WHERE phyla=%s AND family=%s", phyla, family)
// if err != nil {
// 	fmt.Println(err)
// }
// defer rows.Close()

// b := &plant.Plant{}

func main() {

	http.HandleFunc("/", handlerFunc)
	fmt.Println("Starting server .......")

	http.ListenAndServe(":3000", nil)

}
