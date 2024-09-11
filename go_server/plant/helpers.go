package helpers

import (
	"fmt"
	"net/http"
	"os"
	"text/template"
)

type Plant struct {
	CommonName      string   `json:"common_name"`
	ScientificName  string   `json:"scientific_name"`
	Genera          string   `json:"genera"`
	Family          string   `json:"family"`
	Phyla           string   `json:"phyla"`
	Native          bool     `json:"native"`
	Endemic         bool     `json:"endemic"`
	Special         bool     `json:"special"`
	Introduced      bool     `json:"introduced"`
	Invasive        bool     `json:"invasive"`
	CountiesPresent []string `json:"counties_present"`
}
type Query struct {
	queryPhyla          string
	queryFamily         string
	queryGenera         string
	queryCommonName     string
	queryScientificName string
	queryCounties       []string
}

func queryDb(r *http.Request) (results []Plant) {
	r.ParseForm()
	q := Query{
		queryPhyla:          r.FormValue("phyla"),
		queryFamily:         r.FormValue("family"),
		queryGenera:         r.FormValue("genera"),
		queryCommonName:     r.FormValue("common name"),
		queryScientificName: r.FormValue("scientific name"),
		queryCounties:       r.Form["counties"],
	}
	fmt.Println(q.queryCounties)
	tmpl, err := template.ParseFiles("query.tmpl")
	if err != nil {
		panic("template not parsed")
	}
	err = tmpl.Execute(os.Stdout, q)
	if err != nil {
		panic("template not executed.")
	}
	// var query string = `SELECT common_name, scientific_name, genera, family, polyphylactic_group, county_name, native, endemic, special_concern, introduced, invasive FROM species
	// JOIN genera ON genera.genera_id = species.genera_id
	// JOIN family ON family.family_id = species.family_id
	// JOIN phyla ON phyla.phyla_id = species.phyla_id
	// JOIN county_occurance ON county_occurance.species_id = species.species_id
	// JOIN counties ON counties.county_id = county_occurance.county_id
	// WHERE`
	// if len(q.queryCounties) > 0 {
	// 	query = query + "county_name IN " + q.queryCounties
	// }
	// andCheck := query[len(query)-3:]
	// if andCheck == "AND" {

	// }

}

func NewPlant(commonName string, scientificName string, genera string, family string, phyla string, native bool, endemic bool, special bool, introduced bool, invasive bool, counties []string) (Plant, error) {
	if native && invasive {
		err := fmt.Errorf("cannot be both native and invasive")
		return Plant{}, err
	}
	p := Plant{
		CommonName:      commonName,
		ScientificName:  scientificName,
		Genera:          genera,
		Family:          family,
		Phyla:           phyla,
		Native:          native,
		Endemic:         endemic,
		Special:         special,
		Introduced:      introduced,
		Invasive:        invasive,
		CountiesPresent: counties,
	}
	return p, nil
}
