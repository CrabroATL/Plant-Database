package helpers

import (
	"bytes"
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"slices"
	"strconv"
	"strings"
	"text/template"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Plant struct {
	CommonName      string   `json:"common_name"`
	ScientificName  string   `json:"scientific_name"`
	Genera          string   `json:"genera"`
	Family          string   `json:"family"`
	Phyla           string   `json:"phyla"`
	CountiesPresent []string `json:"counties_present"`
	Native          bool     `json:"native"`
	Endemic         bool     `json:"endemic"`
	Special         bool     `json:"special"`
	Introduced      bool     `json:"introduced"`
	Invasive        bool     `json:"invasive"`
}
type Query struct {
	QueryPhyla          string
	QueryFamily         string
	QueryGenera         string
	QueryCommonName     string
	QueryScientificName string
	QueryCounties       []string
}

type AutocompleteData struct {
	Phyla          string
	Family         string
	Genera         string
	CommonName     string
	ScientificName string
}

type AutocompleteReturn struct {
	Phyla           []string `json:"phyla"`
	Family          []string `json:"family"`
	Genera          []string `json:"genera"`
	Common_Name     []string `json:"commonName"`
	Scientific_Name []string `json:"scientificName"`
}

// map[string][]string (use this as the return value later)
func Autocomplete(r *http.Request, data AutocompleteData) (AutocompleteReturn, error) {
	conn, err := pgxpool.New(context.Background(), "postgres://postgres:docker@bridge/plants")
	if err != nil {
		log.Fatalf("Unable to connect to database: %v", err)
	}
	defer conn.Close()

	cleanData := AutocompleteData{
		Phyla:          strings.ToLower(data.Phyla),
		Family:         strings.ToLower(data.Family),
		Genera:         strings.ToLower(data.Genera),
		CommonName:     strings.ToLower(data.CommonName),
		ScientificName: strings.ToLower(data.ScientificName),
	}

	tmpl, err1 := template.ParseFiles("helpers/autocorrect_view_template.tmpl")
	if err1 != nil {
		fmt.Println("parse file error:", err1)
	}
	// if err := tmpl.Execute(os.Stdout, cleanData); err != nil {
	// 	fmt.Println("execute error", err)
	// }
	var query bytes.Buffer
	if err := tmpl.Execute(&query, cleanData); err != nil {
		fmt.Println("execute error:", err)
	}

	qString := query.String()
	n := strings.Count(qString, "?")
	for i := 1; i <= n; i++ {
		i := strconv.Itoa(i)
		qString = strings.Replace(qString, "?", ("$" + i), 1)
	}
	var argstr []any
	if cleanData.Phyla != "" {
		argstr = append(argstr, cleanData.Phyla)
	}
	if cleanData.Family != "" {
		argstr = append(argstr, cleanData.Family)
	}
	if cleanData.Genera != "" {
		argstr = append(argstr, cleanData.Genera)
	}
	if cleanData.CommonName != "" {
		cleanData.CommonName = "%" + cleanData.CommonName + "%"
		argstr = append(argstr, cleanData.CommonName)
	}
	if cleanData.ScientificName != "" {
		cleanData.ScientificName = "%" + cleanData.ScientificName + "%"
		argstr = append(argstr, cleanData.ScientificName)
	}

	fmt.Println(qString)

	checkRows, err := conn.Query(context.Background(), qString, argstr...)
	if err != nil {
		fmt.Println("checkrows err:", err)
	}

	dataStructList, err := pgx.CollectRows(checkRows, pgx.RowToStructByPos[AutocompleteData])
	if err != nil {
		fmt.Println("Collect Rows Err:", err)
	}

	var returnAutocompleteData AutocompleteReturn
	for _, stuff := range dataStructList {
		if !slices.Contains(returnAutocompleteData.Phyla, stuff.Phyla) {
			returnAutocompleteData.Phyla = append(returnAutocompleteData.Phyla, stuff.Phyla)
		}
		if !slices.Contains(returnAutocompleteData.Family, stuff.Family) {
			returnAutocompleteData.Family = append(returnAutocompleteData.Family, stuff.Family)
		}
		if !slices.Contains(returnAutocompleteData.Genera, stuff.Genera) {
			returnAutocompleteData.Genera = append(returnAutocompleteData.Genera, stuff.Genera)
		}
		if !slices.Contains(returnAutocompleteData.Common_Name, stuff.CommonName) {
			returnAutocompleteData.Common_Name = append(returnAutocompleteData.Common_Name, stuff.CommonName)
		}
		if !slices.Contains(returnAutocompleteData.Scientific_Name, stuff.ScientificName) {
			returnAutocompleteData.Scientific_Name = append(returnAutocompleteData.Scientific_Name, stuff.ScientificName)
		}
	}
	return returnAutocompleteData, nil
}

func QueryDb(r *http.Request) ([]Plant, error) {

	r.ParseForm()
	q := Query{
		QueryPhyla:          strings.ToLower(r.FormValue("phyla")),
		QueryFamily:         strings.ToLower(r.FormValue("family")),
		QueryGenera:         strings.ToLower(r.FormValue("genera")),
		QueryCommonName:     strings.ToLower(r.FormValue("common name")),
		QueryScientificName: strings.ToLower(r.FormValue("scientific name")),
		QueryCounties:       r.Form["counties"],
	}
	tmpl, err1 := template.ParseFiles("helpers/query.tmpl")
	if err1 != nil {
		return nil, err1
	}
	if err := tmpl.Execute(os.Stdout, q); err != nil {
		return nil, err
	}
	var qTest bytes.Buffer
	if err := tmpl.Execute(&qTest, q); err != nil {
		return nil, err
	}
	conn, err := pgxpool.New(context.Background(), "postgres://postgres:docker@bridge/plants")
	fmt.Println("conn error:", err)
	if err != nil {
		log.Fatalf("Unable to connect to database: %v", err)
	}
	defer conn.Close()

	// test, err := conn.Exec(context.Background(), "SET search_path TO ar_plants")
	// if err != nil {
	// 	log.Fatal(err)
	// } else {
	// 	fmt.Println(test)
	// }
	qString := qTest.String()
	n := strings.Count(qString, "?")
	for i := 1; i <= n; i++ {
		i := strconv.Itoa(i)
		qString = strings.Replace(qString, "?", ("$" + i), 1)
	}
	var argstr []any
	if q.QueryCommonName != "" {
		q.QueryCommonName = "%" + q.QueryCommonName + "%"
		argstr = append(argstr, q.QueryCommonName)
	}
	if q.QueryScientificName != "" {
		q.QueryScientificName = "%" + q.QueryScientificName + "%"
		argstr = append(argstr, q.QueryScientificName)
	}
	if q.QueryGenera != "" {
		argstr = append(argstr, q.QueryGenera)
	}
	if q.QueryFamily != "" {
		argstr = append(argstr, q.QueryFamily)
	}
	checkRows, err := conn.Query(context.Background(), qString, argstr...)
	if err != nil {
		fmt.Println("Query error:", err)
	}

	plants, err := pgx.CollectRows(checkRows, pgx.RowToStructByPos[Plant])
	if err != nil {
		fmt.Println("collectrows error:", err)
	}

	// add counties query
	// countiesTemplate, err := template.ParseFiles("helpers/counties_template.tmpl")
	// if err != nil {
	// 	fmt.Println("county template error:", err)
	// }

	fmt.Println("pre return check")
	return plants, err1
}
