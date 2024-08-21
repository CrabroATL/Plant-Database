package main

import (
	"encoding/json"
	"fmt"

	"github.com/CrabroATL/Plant-Database/go_server/plant"
)

func main() {
	counties := []string{"yell", "arkansas"}
	p, err := plant.NewPlant("fern", "science fern", true, false, counties)
	if err != nil {
		panic(err)
	}
	fmt.Println(p)
	plantBytes, err := json.MarshalIndent(p, "", "  ")
	if err != nil {
		fmt.Printf("we encountered an error marshalling the json %s\n", err)
	}
	fmt.Println(string(plantBytes))
	fmt.Println(string(plantBytes))
	jsonBytes := []byte(`{
		"common_name": "fern",
		"scientific_name": "science fern",
		"Genera": "",
		"Family": "",
		"Phyla": "",
		"counties_present": [
		  "yell",
		  "arkansas"
		]
	  }`)
	b := &plant.Plant{}
	erro := json.Unmarshal(jsonBytes, b)
	if erro != nil {
		fmt.Println("OhSHIT", erro)
	}
	fmt.Printf("%+v\n", b)
	fmt.Println(b.CountiesPresent)
}
