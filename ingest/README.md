*** Some scripts for convenience. Just as a scratchpad for now ***


curl -XPUT 'localhost:9200/dtdi/mineral-observation/_mapping?pretty' --data-binary @mappings/mineral-observation.json 


curl -XPOST 'localhost:9200/_bulk' --data-binary @[out]



curl -XGET 'localhost:9200/dtdi/mineral-observation/_mapping?pretty'




POST /dtdi/mineral-observation/
{  
  "locality":[  
    {  
      "country":"Canada",
      "region":"Québec, Canada",
      "mine":"Poudrette quarry (Demix quarry; Uni-Mix quarry; Desourdy quarry; Carrière Mont Saint-Hilaire), Mont Saint-Hilaire, La Vallée-du-Richelieu RCM, Montérégie, Québec, Canada",
      "coordinates":{  
        "lat":"45.56277778",
        "lon":"-73.14166667"
      },
      "mindat":"http://www.mindat.org/loc-599.html"
    }
  ],
  "description":"Named after the Abenaki, the indigenous people who inhabited the area around Mont Saint-Hilaire in southern Québec, prior to the arrival of European settlers.",
  "mindat":"http://www.mindat.org/min-2.html",
  "mineral":{  
    "name":"Abenakiite-(Ce)",
    "rruffChemistryConcise":"Na_26_Ce^3+^_6_(SiO_3_)_6_(PO_4_)_6_(CO_3_)_6_(S^4+^O_2_)O",
    "rruffChemistryHTML":"Na<sub>26</sub>Ce<sup>3+</sup><sub>6</sub>(SiO<sub>3</sub>)<sub>6</sub>(PO<sub>4</sub>)<sub>6</sub>(CO<sub>3</sub>)<sub>6</sub>(S<sup>4+</sup>O<sub>2</sub>)O",
    "elements":"Na Ce Si O P C S"
  }
}

DELETE dtdi/mineral-observation

GET /dtdi/mineral-observation/_mapping

GET /dtdi/mineral-observation/_search