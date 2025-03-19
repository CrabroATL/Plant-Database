console.log("js running")

let phyla = document.getElementById("phyla")
let family = document.getElementById("family")
let genera = document.getElementById("genera")
let commonName = document.getElementById("common name")
let scientificName = document.getElementById("scientific name")

function clearList(list) {
    while (list.firstChild) {
        list.removeChild(list.firstChild);
    }
}

function loadDataLists(data) {
    var phylas = document.getElementById("phylas")
    var families = document.getElementById("families")
    var generas = document.getElementById("generas")
    var commonNames = document.getElementById("common names")
    var scientificNames = document.getElementById("scientific names")
    clearList(phylas)
    clearList(families)
    clearList(generas)
    clearList(commonNames)
    clearList(scientificNames)
    if (data.phyla != null) {
        data.phyla.forEach(phyla => {
            const option = document.createElement('option');
            option.value = phyla;
            phylas.appendChild(option)        
        });   
    };
    if (data.family != null) {
        data.family.forEach(family => {
            const option = document.createElement('option');
            option.value = family;
            families.appendChild(option)        
    });
    };
    if (data.genera != null) {
    data.genera.forEach(genera => {
        const option = document.createElement('option');
        option.value = genera;
        generas.appendChild(option)        
    });
    };
    if (data.commonName != null) {
    data.commonName.forEach(commonName => {
        const option = document.createElement('option');
        option.value = commonName;
        commonNames.appendChild(option)        
    });
    };
    if (data.scientificName != null) {
    data.scientificName.forEach(scientificName => {
        const option = document.createElement('option');
        option.value = scientificName;
        scientificNames.appendChild(option)        
    });
    };
}

function getAutoCompleteData() {
    let data = {
        phyla: document.getElementById("phyla").value,
        family: document.getElementById("family").value,
        genera: document.getElementById("genera").value,
        commonName: document.getElementById("common name").value,
        scientificName: document.getElementById("scientific name").value
    }
    
    fetch("http://localhost:3000/", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'content-type':'application/json'
        }
    })
    .then(response => response.json())
    .then (data => loadDataLists(data));
    
}



window.addEventListener("load", getAutoCompleteData)
phyla.addEventListener("focusout", getAutoCompleteData)
family.addEventListener("focusout", getAutoCompleteData)
genera.addEventListener("focusout", getAutoCompleteData)
commonName.addEventListener("focusout", getAutoCompleteData)
scientificName.addEventListener("focusout", getAutoCompleteData)

