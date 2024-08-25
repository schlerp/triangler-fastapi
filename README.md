# Triangler-fastapi

## Data structure

![Triangler-FastAPI Data Model](/.assets/triangler_fastapi_data_model.drawio.png)

## What does the API need to do?

* Administrator users can:
  * maintain experiments
    * create new experiments
    * update existing experiments
    * delete experiments
  * maintain sample flights for experiments
    * create a sample flight
      * generate a token for sample flights
    * update a sample flight
      * generate new token for sample flights
    * delete a sample flight
  * get a report for a given experiment

* anonymous users can:
  * create an observation
    * uses a token to link to the sample
  * update an observation
    * uses the same token again?
    * or should a new one get generated?
