__author__ = 'Hao'

import requests
import csv
import json
import argparse


def printJSONString(x):
    """
    Helper function: take in an un-formatted string, and print properly formatted, indented JSON string
    """
    print(json.dumps(json.loads(x), indent=2, sort_keys=True))


def printJSONPretty(x):
    """
    Helper function: take in a JSON object and print properly formatted, indented JSON string
    """
    print(json.dumps(x, indent=2, sort_keys=True))


def main():
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--es', default="http://localhost:9200", help="elasticsearch service URL")
    parser.add_argument('--mapping', default='../mappings/mineral-observation.json',
                        help='elasticsearch mapping document, e.g. mappings/mineral-observation.json')
    parser.add_argument('out', metavar='OUT', help='elasticsearch bulk ingest file')
    args = parser.parse_args()

    # Open bulk_file to write
    bulk_file = open("bulk_file", "w+")

    # Import IMA mineral list (currently from file)
    mineral_list_reader = csv.DictReader(open("RRUFF_Export.csv", 'r', encoding='utf-8', errors='ignore'))
    mineral_list_JSON_string = json.dumps([x for x in mineral_list_reader], indent=2, sort_keys=True)
    mineral_list_JSON = json.loads(mineral_list_JSON_string)

    # For each mineral in the list:
    # - import the evolution data
    #   - parse the data into mineral observation records in JSON format
    #   = write each mineral observation records into the output

    for mineral_json in mineral_list_JSON[0:10]:

        # Collect info for current mineral species

        mineral_species = json.loads("{}")
        mineral_species["mineral-name-plain"] = mineral_json["Mineral Name (plain)"]
        mineral_species["chemistry-elements-list"] = mineral_json["Chemistry Elements"].strip().split(" ")
        mineral_species["mineral-mindat-url"] = requests.get(
            "http://www.mindat.org/search.php?name=" + mineral_json["Mineral Name (plain)"]).url
        mineral_species["country-of-type-locality"] = mineral_json["Country of Type Locality"]
        mineral_species["fleischers-groupname"] = mineral_json["Fleischers Groupname"]
        mineral_species["ima-chesmistry-html"] = mineral_json["IMA Chemistry (HTML)"]
        mineral_species["ima-chesmistry-concise"] = mineral_json["IMA Chemistry (concise)"]
        mineral_species["ima-number"] = mineral_json["IMA Number"]
        mineral_species["rruff-chemistry-html"] = mineral_json["RRUFF Chemistry (HTML)"]
        mineral_species["rruff-chemistry-concise"] = mineral_json["RRUFF Chemistry (concise)"]
        mineral_species["year-first-published"] = mineral_json["Year First Published"]

        # For current mineral species:
        #   - import evolution dataset, and
        #   - from each locality records, collect data for locality and mineral specimen

        locality_list_reader = csv.DictReader(
            open(mineral_json["Mineral Name (plain)"] + ".csv", 'r', encoding='utf-8', errors='ignore'))
        locality_list_json_string = json.dumps([x for x in locality_list_reader], indent=2, sort_keys=True)
        locality_list_json = json.loads(locality_list_json_string)

        for locality_json in locality_list_json:

            # Rule out evolution data that does not matter
            if locality_json["Label 1"] == "" and locality_json["Label 2"] == "" \
                    and locality_json["MinDat ID"] != locality_json["Dated Locality ID"]:
                continue

            # Collect locality
            locality = json.loads("{}")
            locality["locality-label"] = locality_json["Locality containing Mineral"]
            locality["locality-mindat-id"] = str(locality_json["MinDat ID"])
            locality["locality-mindat-url"] = "http://www.mindat.org/loc-" + locality_json["MinDat ID"] + ".html"
            _country_region = locality_json["Locality containing Mineral"].strip().split(",")
            locality["country"] = _country_region[len(_country_region) - 1].strip()
            locality["region"] = _country_region[len(_country_region) - 2].strip() + ", " + _country_region[
                len(_country_region) - 1].strip()
            locality["lat"] = int(locality_json["Lat Deg"]) + int(locality_json["Lat Min"]) / 60 + int(
                locality_json["Lat Sec"]) / 3600
            locality["lon"] = int(locality_json["Lon Deg"]) + int(locality_json["Lon Min"]) / 60 + int(
                locality_json["Lon Sec"]) / 3600
            locality["lat-deg"] = locality_json["Lat Deg"]
            locality["lat-min"] = locality_json["Lat Min"]
            locality["lat-sec"] = locality_json["Lat Sec"]
            locality["lon-deg"] = locality_json["Lon Deg"]
            locality["lon-min"] = locality_json["Lon Min"]
            locality["lon-sec"] = locality_json["Lon Sec"]
            locality["coordinates"] = locality_json["Decimal Degree"]

            # Collect mineral specimen
            mineral_specimen = json.loads("{}")
            mineral_specimen["age-unit"] = "Ma"
            if locality_json["Max Age (Ma)"] is not "":
                mineral_specimen["max-age"] = float(locality_json["Max Age (Ma)"])
            if locality_json["Min Age (Ma)"] is not "":
                mineral_specimen["min-age"] = float(locality_json["Min Age (Ma)"])
            mineral_specimen["dated-locality-label"] = locality_json["Dated Locality (Max Age)"]
            mineral_specimen["dated-locality-mindat-id"] = str(locality_json["Dated Locality ID"])
            mineral_specimen["dated-locality-mindat-url"] = "http://www.mindat.org/loc-" + locality_json[
                "Dated Locality ID"] + ".html"

            age_determination_process = json.loads('{"mindat-claims-existence":{},"remote-age":{},"age-info":{}}')

            if locality_json["Label 1"] is not "":
                age_determination_process["mindat-claims-existence"]["label"] = locality_json["Label 1"]
                age_determination_process["mindat-claims-existence"]["description"] = "Mindat claims that this mineral occurs at this locality."
            else:
                age_determination_process["mindat-claims-existence"]["label"] = ""
                age_determination_process["mindat-claims-existence"]["description"] = "Mindat does not claim that this mineral occurs at this locality."

            if locality_json["Label 2"] is not "":
                age_determination_process["remote-age"]["label"] = locality_json["Label 2"]
                age_determination_process["remote-age"]["description"] = "The age displayed for this mineral is coming from a different, non-child locality."
            else:
                age_determination_process["remote-age"]["label"] = ""
                age_determination_process["remote-age"]["description"] = "The age displayed for this mineral is coming the same locality."

            if locality_json["Label 3"] is "G":
                age_determination_process["age-info"]["label"] = "G"
                age_determination_process["age-info"]["description"] = "This mineral is directly dated."
            if locality_json["Label 3"] is "B":
                age_determination_process["age-info"]["label"] = "B"
                age_determination_process["age-info"]["description"] = "This mineral is explicitely specified as having an age."
            if locality_json["Label 3"] is "Y":
                age_determination_process["age-info"]["label"] = "Y"
                age_determination_process["age-info"]["description"] = "This mineral is using an age from a mineralization period."
            if locality_json["Label 3"] is "O":
                age_determination_process["age-info"]["label"] = "O"
                age_determination_process["age-info"]["description"] = "This mineral is using an age calculated from all data at the locality."
            if locality_json["Label 3"] is "":
                age_determination_process["age-info"]["label"] = ""
                age_determination_process["age-info"]["description"] = "This mineral is not associated with an age."


            mineral_specimen["age-determination-process"] = age_determination_process

            # Put mineral and locality info into mineral_observation object
            mineral_observation = json.loads("{}")
            mineral_observation["mineral-species"] = mineral_species
            mineral_observation["locality"] = locality
            mineral_observation["mineral-specimen"] = mineral_specimen


            # Write current mineral observation object to output
            bulk_file.write('{"index":{"_type":"mineral-observation","_index":"dtdi"}}\n')
            bulk_file.write(json.dumps(mineral_observation) + "\n")


    bulk_file.close()


if __name__ == "__main__":
    main()