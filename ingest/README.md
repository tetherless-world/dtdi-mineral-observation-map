***This is temporarily a scratch pad and will be a formatted README as it goes on***

### Installing Instructions

1. To generate bulk-file, change directory to `dtdi-mineral-observation-map/ingest/example` and execute:

`python3 parseOriginalData.py` 

A bulk upload file called `bulk-file` will be generated.

2. To upload file to elasticsearch:

(1) Delete the existing data and mapping: `curl -XDELETE 'localhost:9200/dtdi/mineral-observation'`

(2) Upload the mapping file:
`curl -XPUT 'localhost:9200/dtdi/mineral-observation/_mapping?pretty' --data-binary @../mappings/mineral-observation-new.json`

(3) Upload the bulk file:
`curl -XPOST 'localhost:9200/_bulk' --data-binary @bulk_file`

====================================================================
** Below are scratches and miscellaneous info. Please ignore for now**

1) Go to http://rruff.info/ima/ and log in.

2) Select "IMA Approved Minerals Only"

3) Export Minerals. Export Options: (Below are the useful ones, almost is everything)

  - Mineral Name (plain)
  - RRUFF Chemistry (plain)
  - RRUFF Chemistry (concise)
  - IMA Chesmistry (plain)
  - IMA Chesmistry (concise)
  - Chemical Elements
  - RRUFF IDs
  - IMA Number
  - Database ID***?
  - Country 
  - Structural Groupname
  - Fleischers Groupname
  - IMA Status
  - Status Notes
  - Year First Published

Mindat link: www.mindat.org/search.php?name=Abelsonite
or: http://www.mindat.org/show.php?name=Abelsonite

4) Export Evolution Records for each minerals
First go to http://rruff.info/mineral_list/locality.php?mineral_name=xxxxxxxxxxx(the mineral name, not case-sensitive)
Click "Show GPS"
Click "Export Table"
Save the data from the 3rd column to an csv file. ()

Locality IDs:
http://rruff.info/mineral_list/locality.php?mindat_id=20265
http://www.mindat.org/loc-20265.html




Does these matter in the future
    This age satisfies at least one of these three conditions:
1) Mindat claims that this mineral occurs at this locality.
2) The locality containing the mineral has an age directly assigned to it.
3) This locality is displaying an age from a non-child locality.
    This age does not satisfy any of the above conditions.

 G  This mineral is directly dated.
 B  This mineral is explicitely specified as having an age.
 Y  This mineral is using an age from a mineralization period.
 O  This mineral is using an age calculated from all data at the locality.
 R  The age displayed for this mineral is coming from a different, non-child locality.
  This mineral is not associated with an age.






*** Some scripts for convenience. Just as a scratchpad for now ***


curl -XPUT 'localhost:9200/dtdi/mineral-observation/_mapping?pretty' --data-binary @mappings/mineral-observation.json 


curl -XPOST 'localhost:9200/_bulk' --data-binary @[out]

curl -XGET 'localhost:9200/dtdi/mineral-observation/_mapping?pretty'

DELETE dtdi/mineral-observation

GET /dtdi/mineral-observation/_mapping

GET /dtdi/mineral-observation/_search