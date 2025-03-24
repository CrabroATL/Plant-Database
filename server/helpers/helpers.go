package helpers

import (
	"bytes"
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
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

func Autocomplete(r *http.Request) map[string][]string {
	conn, err := pgxpool.New(context.Background(), "postgres://postgres:password@localhost:30420/plants")
	if err != nil {
		log.Fatalf("Unable to connect to database: %v", err)
	}
	defer conn.Close()
	test, err := conn.Exec(context.Background(), "SET search_path TO ar_plants")
	if err != nil {
		log.Fatal(err)
	} else {
		fmt.Println(test)
	}

	familyAC, err := conn.Query(context.Background(), "SELECT family FROM family")
	if err != nil {
		log.Fatal(err)
	}
	generaAC, err := conn.Query(context.Background(), "SELECT genera FROM ar_plants.genera")
	if err != nil {
		log.Fatal(err)
	}
	commonAC, err := conn.Query(context.Background(), "SELECT common_name FROM ar_plants.species")
	if err != nil {
		log.Fatal(err)
	}
	scienceAC, err := conn.Query(context.Background(), "SELECT scientific_name FROM ar_plants.species")
	if err != nil {
		log.Fatal(err)
	}
	familyData, err := pgx.CollectRows(familyAC, pgx.RowToMap)
	if err != nil {
		log.Fatal(err)
	}
	generaData, err := pgx.CollectRows(generaAC, pgx.RowToMap)
	if err != nil {
		log.Fatal(err)
	}
	commonNameData, err := pgx.CollectRows(commonAC, pgx.RowToMap)
	if err != nil {
		log.Fatal(err)
	}
	ScientificNameData, err := pgx.CollectRows(scienceAC, pgx.RowToMap)
	if err != nil {
		log.Fatal(err)
	}

	var familyList []string
	for _, m := range familyData {
		for _, v := range m {
			familyList = append(familyList, v.(string))
		}
	}
	var generaList []string
	for _, m := range generaData {
		for _, v := range m {
			generaList = append(generaList, v.(string))
		}
	}
	var commonNameList []string
	for _, m := range commonNameData {
		for _, v := range m {
			commonNameList = append(commonNameList, v.(string))
		}
	}
	var scientificNameList []string
	for _, m := range ScientificNameData {
		for _, v := range m {
			scientificNameList = append(scientificNameList, v.(string))
		}
	}
	fullMap := map[string][]string{
		"family":         familyList,
		"genera":         generaList,
		"commonName":     commonNameList,
		"scientificName": scientificNameList,
	}

	return fullMap
}

func QueryDb(r *http.Request) ([]Plant, error) {

	r.ParseForm()
	q := Query{
		QueryPhyla:          r.FormValue("phyla"),
		QueryFamily:         strings.ToLower(r.FormValue("family")),
		QueryGenera:         strings.ToLower(r.FormValue("genera")),
		QueryCommonName:     strings.ToLower(r.FormValue("common name")),
		QueryScientificName: strings.ToLower(r.FormValue("scientific name")),
		QueryCounties:       r.Form["counties"],
	}
	tmpl, err1 := template.ParseFiles("helpers/query.tmpl")
	fmt.Println("check")
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
	conn, err := pgxpool.New(context.Background(), "postgres://postgres:password@localhost:30420/postgres")
	fmt.Println(err)
	if err != nil {
		log.Fatalf("Unable to connect to database: %v", err)
	}
	defer conn.Close()

	test, err := conn.Exec(context.Background(), "SET search_path TO ar_plants")
	if err != nil {
		log.Fatal(err)
	} else {
		fmt.Println(test)
	}
	qString := qTest.String()
	n := strings.Count(qString, "?")
	for i := 1; i <= n; i++ {
		i := strconv.Itoa(i)
		qString = strings.Replace(qString, "?", ("$" + i), 1)
	}
	var argstr []any
	if q.QueryCommonName != "" {
		argstr = append(argstr, q.QueryCommonName)
	}
	if q.QueryScientificName != "" {
		argstr = append(argstr, q.QueryScientificName)
	}
	if q.QueryGenera != "" {
		argstr = append(argstr, q.QueryGenera)
	}
	if q.QueryFamily != "" {
		argstr = append(argstr, q.QueryFamily)
	}
	fmt.Println(qString)
	checkRows, err := conn.Query(context.Background(), qString, argstr...)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(checkRows)

	plants, err := pgx.CollectRows(checkRows, pgx.RowToStructByPos[Plant])
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println("pre return check")
	return plants, err1
}
