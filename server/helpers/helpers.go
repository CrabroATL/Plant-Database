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
	CommonName      string `json:"common_name"`
	ScientificName  string `json:"scientific_name"`
	Genera          string `json:"genera"`
	Family          string `json:"family"`
	Phyla           string `json:"phyla"`
	CountiesPresent string `json:"counties_present"`
	Native          bool   `json:"native"`
	Endemic         bool   `json:"endemic"`
	Special         bool   `json:"special"`
	Introduced      bool   `json:"introduced"`
	Invasive        bool   `json:"invasive"`
}
type Query struct {
	QueryPhyla          string
	QueryFamily         string
	QueryGenera         string
	QueryCommonName     string
	QueryScientificName string
	QueryCounties       []string
}

func QueryDb(r *http.Request) ([]Plant, error) {

	r.ParseForm()
	q := Query{
		QueryPhyla:          r.FormValue("phyla"),
		QueryFamily:         r.FormValue("family"),
		QueryGenera:         r.FormValue("genera"),
		QueryCommonName:     r.FormValue("common name"),
		QueryScientificName: r.FormValue("scientific name"),
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
	var counter int
	if q.QueryCommonName != "" {
		argstr = append(argstr, q.QueryCommonName)
		counter += 1
	}
	if q.QueryScientificName != "" {
		argstr = append(argstr, q.QueryScientificName)
		counter += 1
	}
	if q.QueryGenera != "" {
		argstr = append(argstr, q.QueryGenera)
		counter += 1
	}
	if q.QueryFamily != "" {
		argstr = append(argstr, q.QueryFamily)
		counter += 1
	}
	fmt.Println(qString)
	checkQuery, err := conn.Query(context.Background(), qString, argstr...)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(checkQuery)

	plants, err := pgx.CollectRows(checkQuery, pgx.RowToStructByPos[Plant])
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println("pre return check")
	return plants, err1
}
