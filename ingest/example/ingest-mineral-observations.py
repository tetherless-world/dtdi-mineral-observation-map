__author__ = 'Hao'

import requests
import csv
import json
import argparse


GEOLOGIC_TIME_SERVICE_URL = "https://deeptime.tw.rpi.edu/geologic-intervals/resolve-intersects"


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

    # Import IMA mineral list (currently from file)
    mineral_list_reader = csv.DictReader(open("RRUFF_Export.csv", 'r', encoding='utf-8', errors='ignore'))
    mineral_list_JSON_string = json.dumps([x for x in mineral_list_reader], indent=2, sort_keys=True)
    mineral_list_JSON = json.loads(mineral_list_JSON_string)

    # For each mineral in the list:
    # - import the evolution data
    #   - parse the data into mineral observation records in JSON format
    #   = write each mineral observation records into the output

    with open(args.out, "w+") as bulk_file:

        for mineral_json in mineral_list_JSON[0:10]:
            # Collect info for current mineral species

            mineral = json.loads("{}")
            mineral["mineral-name-plain"] = mineral_json["Mineral Name (plain)"]
            mineral["chemistry-elements-list"] = mineral_json["Chemistry Elements"].strip().split(" ")
            mineral["mineral-mindat-url"] = requests.get(
                "http://www.mindat.org/search.php?name=" + mineral_json["Mineral Name (plain)"]).url
            mineral["country-of-type-locality"] = mineral_json["Country of Type Locality"]
            mineral["fleischers-groupname"] = mineral_json["Fleischers Groupname"]
            mineral["ima-chesmistry-html"] = mineral_json["IMA Chemistry (HTML)"]
            mineral["ima-chesmistry-concise"] = mineral_json["IMA Chemistry (concise)"]
            mineral["ima-number"] = mineral_json["IMA Number"]
            mineral["rruff-chemistry-html"] = mineral_json["RRUFF Chemistry (HTML)"]
            mineral["rruff-chemistry-concise"] = mineral_json["RRUFF Chemistry (concise)"]
            mineral["year-first-published"] = mineral_json["Year First Published"]

            # For current mineral species:
            #   - import evolution dataset, and
            #   - from each locality records, collect data for locality and mineral specimen

            locality_list_reader = csv.DictReader(
                open(mineral_json["Mineral Name (plain)"] + ".csv", 'r', encoding='utf-8', errors='ignore'))
            locality_list_json_string = json.dumps([x for x in locality_list_reader], indent=2, sort_keys=True)
            locality_list_json = json.loads(locality_list_json_string)

            for locality_json in locality_list_json:

                # Collect locality
                locality = json.loads("{}")
                locality["locality-label"] = locality_json["Locality containing Mineral"]
                locality["locality-mindat-id"] = locality_json["MinDat ID"]
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

                if locality_json["Max Age (Ma)"] is not "": locality["max-age"] = float(locality_json["Max Age (Ma)"])
                if locality_json["Min Age (Ma)"] is not "": locality["min-age"] = float(locality_json["Min Age (Ma)"])

                if locality_json["Max Age (Ma)"] is not "" and locality_json["Min Age (Ma)"] is not "":
                    # https://deeptime.tw.rpi.edu/geologic-intervals/resolve-intersects
                    min_age = float(locality_json["Min Age (Ma)"])
                    max_age = float(locality_json["Max Age (Ma)"])
                    payload = {'min': min_age, 'max': max_age }
                    r = requests.get(GEOLOGIC_TIME_SERVICE_URL, params=payload)
                    geologic_time_info = r.json()

                    geologic_time = json.loads("{}")

                    geologic_time["eon"] = [interval["nam"] for interval in geologic_time_info if interval["type"] == "Eon"]
                    geologic_time["era"] = [interval["nam"] for interval in geologic_time_info if interval["type"] == "Era"]
                    geologic_time["period"] = [interval["nam"] for interval in geologic_time_info if interval["type"] == "Period"]
                    geologic_time["epoch"] = [interval["nam"] for interval in geologic_time_info if interval["type"] == "Epoch"]
                    geologic_time["stage"] = [interval["nam"] for interval in geologic_time_info if interval["type"] == "Stage"]

                    locality["geologic_time"] = geologic_time

                locality["dated-locality-label"] = locality_json["Dated Locality (Max Age)"]
                locality["dated-locality-mindat-id"] = locality_json["Dated Locality ID"]
                locality["dated-locality-mindat-url"] = "http://www.mindat.org/loc-" + locality_json[
                    "Dated Locality ID"] + ".html"

                # Put mineral and locality info into mineral_observation object
                mineral_observation = json.loads("{}")
                mineral_observation["mineral"] = mineral
                mineral_observation["locality"] = locality


                # Write current mineral observation object to output
                bulk_file.write('{"index":{"_type":"mineral-observation","_index":"dtdi"}}\n')
                bulk_file.write(json.dumps(mineral_observation) + "\n")


if __name__ == "__main__":
    main()