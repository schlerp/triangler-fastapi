# triangler-fastapi

## What does the API need to do?

* admin users can:
  * maintain experiments
    * create new experiments
    * update existing experiments
    * delete experiments
  * maintain samples for experiments
    * create a sample
      * generate a token for samples
    * update a sample
      * generate new token for samples
    * delete a sample
  * get a report for a given experiment

* anonymous users can:
  * create an observation
    * uses a token to link to the sample
  * update an observation
    * uses the same token again?
    * or should we gen a new one?
