package main

import (
	"fmt"
	"html/template"
	"net/http"

	"github.com/CrabroATL/Plant-Database/server/helpers"
)

func searchResults(w http.ResponseWriter, r *http.Request) {
	plants, err := helpers.QueryDb(r)
	if err != nil {
		panic(err)
	}
	fmt.Println("Search results test")
	for _, plant := range plants {
		fmt.Printf("%+v\n", plant)
	}
	fmt.Println("post struct check")
	tmpl := make(map[string]*template.Template)
	tmpl["results.html"] = template.Must(template.ParseFiles("results.html", "layout.html"))
	tmpl["results.html"].ExecuteTemplate(w, "layout", plants)
}

func mainPage(w http.ResponseWriter, r *http.Request) {
	fmt.Println("in main page")
	tmpl := make(map[string]*template.Template)
	fullMap := helpers.Autocomplete(r)
	tmpl["index.html"] = template.Must(template.ParseFiles("index.html", "layout.html"))
	tmpl["index.html"].ExecuteTemplate(w, "layout", fullMap)
}

func main() {

	http.HandleFunc("/", mainPage)
	http.HandleFunc("/search", searchResults)
	fmt.Println("Starting server .......")
	err := http.ListenAndServe(":3000", nil)
	if err != nil {
		fmt.Print(err)
	}
}
