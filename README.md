# cricket-analytics

This is a simple analytics project which can be potentially used to analyze various players and their performances in the past. The project is created for the people who wants to understand basics of data engineering. I have kept things very simple for this project but I am going to specify what equivalent cloud technology or method is used in the industry. Happy learning!! 

### Components associated with the project:
1. Extracting Data
2. Data cleaning (Transaformations)
3. Loading Data
4. Performing Analytics

### Extracting Data
In order to understand cricket data, the first step is to obtain the data. We are going to get the data from https://cricsheet.org/. Here are can obtain data in `json` format. 

#### Notes: 
For extraction, we are not using scraping or APIs for the project. In real world scenario, there can be multiple ways to obtain the data:
1. REST API
2. Database systems
3. SFTP
4. IOT devices
5. Cloud storage

Depending on the infrastructure and usecase, there can be a any such data souce. 

In order to keep things simplified, we are going to download the data as a zip file and then extract the data on a perticular location on the local machine. 

Another option is to simulate cloud storage (s3) locally and extract data from there, i have explained how it can be done in [this article](https://vasav.co.in/blog/localstack/).

#### Steps:
- Find data-processing-config.json file and update the following keys
```commandline
{
  "data-dir": "E:\\cricket-analytics\\ipl_json\\",
  "processed-data-dir": "E:\\cricket-analytics\\ipl_json\\processed_data\\"
}
```

`data-dir` contains all the source json files while `processed-data-dir` will have the processed file. 

### Transforming Data
#### Notes:
For simplicity, we are just listing files in the folder and then processing them sequentially. In realworld scenario, especially for large scaled data apache spark like distributed computing framework is used. 

There is a need of delta logic if we are running the transformation on daily basis. In the real world, batch processing is done at a schedule. When we are processing may files (at scale of thousands or millions), we have to make sure we are not processing same files again. So a delta logic needs to be placed which keeps track of the files which are already processed and identify the new files to be processed from the cloud. 
This is an important thing to save resources and eliminating unwanted processing of the data.

#### Steps:
This step is going to convert the json file to a tabular data where every row represents 1 delivery. So it is a ball by ball data for the match. 

1. Create a virtual environment by command `python -m venv venv`
2. Install all the dependencies using `pip install -r requirements.txt`
3. Run the `python -m baseapp.cricket-data-processing.cricket_match_data_processing_job` command to run the python script from root dir (cricket-analytics)
4. You will see all the processed csv file in the path specified in the json config file.

### Loading Data

TODO: Perform DB insertion 

### Analysis

TODO: Create a dashboard using a tool like metabase or apache superset. 