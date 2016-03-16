## Ingest Instructions

#### Step 1 Generate JSON file

Change directory to 

`dtdi-mineral-observation-map/ingest/example` 

and execute

`python3 ingest-mineral-observations.py [output]` 

A file called `[output]` will be generated.

#### Step 2 Upload file to elasticsearch

* Delete the existing data and mapping: 

`curl -XDELETE 'localhost:9200/dtdi/mineral-observation'`

* Upload the mapping file:

`curl -XPUT 'localhost:9200/dtdi/mineral-observation/_mapping?pretty' --data-binary @../mappings/mineral-observation-new.json`

* Upload the bulk file:

`curl -XPOST 'localhost:9200/_bulk' --data-binary @bulk_file`



## Exporting Data from RRUFF IMA Database UI

1. Go to [http://rruff.info/ima/] and log in.

2. Select "IMA Approved Minerals Only"

3. Export IMA mineral list to a CSV file. Export Options: (Below are the useful ones, almost is everything)

    - Mineral Name (plain)
    - RRUFF Chemistry (plain)
    - RRUFF Chemistry (concise)
    - IMA Chesmistry (plain)
    - IMA Chesmistry (concise)
    - Chemical Elements
    - RRUFF IDs
    - IMA Number
    - Database ID
    - Country 
    - Structural Groupname
    - Fleischers Groupname
    - IMA Status
    - Status Notes
    - Year First Published
    
4. Manually export Evolution Records for each minerals (e.g. Abelsonite)

    - First go to `http://rruff.info/mineral_list/locality.php?mineral_name=abelsonite`
    - Click "Show GPS"
    - Click "Export Table"
    - Save the data to a csv file, named `Abelsonite.csv`



## Miscellaneous Notes

* For each mineral, say Abelsonite, 'www.mindat.org/search.php?name=Abelsonite' or
    'http://www.mindat.org/show.php?name=Abelsonite' will be redirected to its page on mindat.


* Given a locality ID, 'http://rruff.info/mineral_list/locality.php?mindat_id=20265'
    or 'http://www.mindat.org/loc-20265.html' will be redirected to its page on mindat.
