package main

import (
	"encoding/json"
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
		fmt.Printf("plant range check: %+v\n", plant)
	}
	// plantsJson, err := json.Marshal(plants)
	// if err != nil {
	// 	fmt.Println(err)
	// }
	fmt.Printf("plants struct check: %+v", plants)
	tmpl := make(map[string]*template.Template)
	tmpl["results.html"] = template.Must(template.ParseFiles("static/results.html", "static/layout.html"))
	tmpl["results.html"].ExecuteTemplate(w, "layout", plants)
}

func mainPage(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		tmpl := make(map[string]*template.Template)
		tmpl["index.html"] = template.Must(template.ParseFiles("static/index.html", "static/layout.html"))
		tmpl["index.html"].ExecuteTemplate(w, "layout", nil)
	case "POST":
		fmt.Println("POST running")
		var test helpers.AutocompleteData
		json.NewDecoder(r.Body).Decode(&test)

		returnStruct, err := helpers.Autocomplete(r, test)
		if err != nil {
			fmt.Print("aurocompelte return error:", err)
		}
		returnJSON, err := json.Marshal(returnStruct)
		if err != nil {
			fmt.Println("Json Marshal error:", err)
		}
		w.Write(returnJSON)
	}

}

func main() {

	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static", fs))
	http.HandleFunc("/", mainPage)
	http.HandleFunc("/search", searchResults)
	fmt.Println("Starting server .......")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Print("Listen and serve error:", err)
	}
}
