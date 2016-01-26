import requests
import csv, json

def printJSONString(x):
	y = json.loads(x)
	print(json.dumps(json.loads(x), indent=2, sort_keys=True))

def printJSONPretty(x):
	print(json.dumps(x, indent=2, sort_keys=True))


es_index_line = '{"index":{"_type":"mineral-observation","_index":"dtdi"}}\n'

mineral_observations_file = open("mineral_observations.csv", 'w+')
bulk_file = open("bulk", "w+")

mineral_list_reader = csv.DictReader(open("RRUFF_Export.csv", 'r', encoding='utf-8', errors='ignore'))
mineral_list_json_string = json.dumps([x for x in mineral_list_reader ], indent=2, sort_keys=True)
# print(mineral_list_json_string[0:750])
mineral_list_json = json.loads(mineral_list_json_string)
# print([x['Mineral Name'] for x in mineral_list_json[0:10]])

mineral_observations = []
for mineral_json in mineral_list_json[0:10]:
	mineral_json["mineral-name-plain"] = mineral_json["Mineral Name (plain)"]
	# Create Chemistry Elements List
	mineral_json["Chemistry Elements List"] = mineral_json["Chemistry Elements"].strip().split(" ")
	# Create Mindat-based URI for the mineral
	mineral_json["Mineral Mindat"] = requests.get("http://www.mindat.org/search.php?name=" + mineral_json["Mineral Name (plain)"]).url
	# Now we have mineral information ready.
	# We go through each observation from the locality list, and generate mineral observation records
	locality_list_reader = csv.DictReader(open(mineral_json["Mineral Name (plain)"] + ".csv", 'r', encoding='utf-8', errors='ignore'))
	locality_list_json_string = json.dumps([x for x in locality_list_reader ], indent=2, sort_keys=True)
	locality_list_json = json.loads(locality_list_json_string)
	for locality_json in locality_list_json:
		# Adding some locality properties
		locality_json["Locality Mindat"] = "http://www.mindat.org/loc-" + locality_json["MinDat ID"] + ".html"
		locality_json["Lat"] = int(locality_json["Lat Deg"]) + int(locality_json["Lat Min"])/60 + int(locality_json["Lat Sec"])/3600
		locality_json["Lon"] = int(locality_json["Lon Deg"]) + int(locality_json["Lon Min"])/60 + int(locality_json["Lon Sec"])/3600
		_country_region = locality_json["Locality containing Mineral"].strip().split(",")
		locality_json["Country"] = _country_region[len(_country_region)-1].strip()		
		locality_json["Region"] =  _country_region[len(_country_region)-2].strip() + ", " + _country_region[len(_country_region)-1].strip()
		# Put mineral and locality info into mineral_observation
		mineral_observation = json.loads('{"mineral":{},"locality":{}}')
		mineral_observation["mineral"] = mineral_json
		mineral_observation["locality"] = locality_json
		# Next, append to min-obs list and complete one entry, and also add item to bulk
		bulk_file.write(es_index_line)
		bulk_file.write(json.dumps(mineral_observation) + "\n")
		mineral_observations.append(mineral_observation)


print(json.dumps(mineral_observations[0], indent=2, sort_keys=True))
print(len(mineral_observations))

