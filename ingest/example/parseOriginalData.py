import requests
import csv, json


def printJSONString(x):
	print(json.dumps(json.loads(x), indent=2, sort_keys=True))


def printJSONPretty(x):
	print(json.dumps(x, indent=2, sort_keys=True))


es_index_line = '{"index":{"_type":"mineral-observation","_index":"dtdi"}}\n'


# Open bulk_file to write
bulk_file = open("bulk_file", "w+")


mineral_list_reader = csv.DictReader(open("RRUFF_Export.csv", 'r', encoding='utf-8', errors='ignore'))
mineral_list_JSON_string = json.dumps([x for x in mineral_list_reader ], indent=2, sort_keys=True)
mineral_list_JSON = json.loads(mineral_list_JSON_string)


mineral_observations = []
for mineral_json in mineral_list_JSON[0:10]:
	mineral_species = json.loads("{}")
	# print(mineral_json["Mineral Name (plain)"])
	mineral_species["mineral-name-plain"] = mineral_json["Mineral Name (plain)"]
	mineral_species["chemistry-elements-list"] = mineral_json["Chemistry Elements"].strip().split(" ")
	mineral_species["mineral-mindat-url"] = requests.get("http://www.mindat.org/search.php?name=" + mineral_json["Mineral Name (plain)"]).url
	mineral_species["country-of-type-locality"] = mineral_json["Country of Type Locality"]
	mineral_species["fleischers-groupname"] = mineral_json["Fleischers Groupname"]
	mineral_species["ima-chesmistry-html"] = mineral_json["IMA Chemistry (HTML)"]
	mineral_species["ima-chesmistry-concise"] = mineral_json["IMA Chemistry (concise)"]
	mineral_species["ima-number"] = mineral_json["IMA Number"]
	mineral_species["rruff-chemistry-html"] = mineral_json["RRUFF Chemistry (HTML)"]
	mineral_species["rruff-chemistry-concise"] = mineral_json["RRUFF Chemistry (concise)"]
	mineral_species["year-first-published"] = mineral_json["Year First Published"]

	# Now we have mineral information ready.
	# We go through each observation from the locality list, and generate mineral observation records
	locality_list_reader = csv.DictReader(open(mineral_json["Mineral Name (plain)"] + ".csv", 'r', encoding='utf-8', errors='ignore'))
	locality_list_json_string = json.dumps([x for x in locality_list_reader ], indent=2, sort_keys=True)
	locality_list_json = json.loads(locality_list_json_string)
	for locality_json in locality_list_json:
		locality = json.loads("{}")
		locality["locality-label"] 	= locality_json["Locality containing Mineral"]
		locality["locality-mindat-id"]  = locality_json["MinDat ID"]
		locality["locality-mindat-url"] = "http://www.mindat.org/loc-" + locality_json["MinDat ID"] + ".html"
		_country_region = locality_json["Locality containing Mineral"].strip().split(",")
		locality["country"] = _country_region[len(_country_region)-1].strip()
		locality["region"] =  _country_region[len(_country_region)-2].strip() + ", " + _country_region[len(_country_region)-1].strip()
		locality["lat"] = int(locality_json["Lat Deg"]) + int(locality_json["Lat Min"])/60 + int(locality_json["Lat Sec"])/3600
		locality["lon"] = int(locality_json["Lon Deg"]) + int(locality_json["Lon Min"])/60 + int(locality_json["Lon Sec"])/3600
		locality["lat-deg"] = int(locality_json["Lat Deg"])
		locality["lat-min"] = int(locality_json["Lat Min"])
		locality["lat-sec"] = int(locality_json["Lat Sec"])
		locality["lon-deg"] = int(locality_json["Lon Deg"])
		locality["lon-min"] = int(locality_json["Lon Min"])
		locality["lon-sec"] = int(locality_json["Lon Sec"])
		locality["coordinates"] = locality_json["Decimal Degree"]
		locality["dated-locality-label"] = locality_json["Dated Locality (Max Age)"]
		locality["dated-locality-mindat-id"]  = locality_json["Dated Locality ID"]
		locality["dated-locality-mindat-url"] = "http://www.mindat.org/loc-" + locality_json["Dated Locality ID"] + ".html"
		mineral_specimen = json.loads("{}")
		if locality_json["Max Age (Ma)"] is not "": mineral_specimen["max-age"] = float(locality_json["Max Age (Ma)"])
		if locality_json["Min Age (Ma)"] is not "": mineral_specimen["min-age"] = float(locality_json["Min Age (Ma)"])
		if locality_json["Label 1"] is not "": mineral_specimen["label-1"] = locality_json["Label 1"]
		if locality_json["Label 2"] is not "": mineral_specimen["label-2"] = locality_json["Label 2"]
		if locality_json["Label 3"] is not "": mineral_specimen["label-3"] = locality_json["Label 3"]
		# Put mineral and locality info into mineral_observation
		mineral_observation = json.loads('{}')
		mineral_observation["mineral-species"] = mineral_species
		mineral_observation["locality"] = locality
		mineral_observation["mineral-specimen"] = mineral_specimen
		# Next, append to min-obs list and complete one entry, and also add item to bulk
		bulk_file.write(es_index_line)
		bulk_file.write(json.dumps(mineral_observation) + "\n")
		mineral_observations.append(mineral_observation)


print(json.dumps(mineral_observations[2], indent=2, sort_keys=True))
# print(len(mineral_observations))

