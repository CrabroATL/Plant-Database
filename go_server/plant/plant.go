package plant

import (
	"context"
	"fmt"
	"os"

	"github.com/jackc/pgx/v5"
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

func NewPlant(commonName string, scientificName string, native bool, invasive bool, counties []string) (Plant, error) {
	conn, err := pgx.Connect(context.Background(), os.Getenv("postgres://postgres:postgres@postgres:5432/postgres"))
	if native && invasive {
		err := fmt.Errorf("cannot be both native and invasive")
		return Plant{}, err
	}
	conn = conn
	err = err
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
