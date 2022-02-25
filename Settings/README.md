# Mongo DB Config
This application is intended to config the collections' initial version. 
The operator runs it once to initialize the database with default values.

## System Requirements

- Windows 7/8/10
- [Python 3.8.3 - 32bits](https://www.python.org/downloads/release/python-383/)

## Installing

To install the Python virtual environment and its dependencies, run `install.bat`.

## Configuring

Before run the script it's necessary to configure the `config.yaml` file in `db-config` directory.
```bash
  databases:
  - db_name: "DATABASE NAME"
    db_host: 127.0.0.1
    db_port: 27017
    db_user: "DATABASE USER"
    db_pass: "DATABASE PASSWORD"
```

An example:
```bash
databases:
  - db_name: pythia
    db_host: localhost
    db_port: 27017
    db_user: ''
    db_pass: ''
```
Another file to be configured is related to the tags of each system.
For each system is necessary a file.

```bash
database: "DATABASE NAME"
documents:
  - server: "SERVER 1"
    tags:
      - id: "TAG_SERVER1_ID"
        name: "TAG SERVER1 NAME"

  - server: "SERVER 2"
    tags:
      - id: "TAG_SERVER2_ID"
        name: "TAG SERVER2 NAME"
```

An example:
```bash
database: pythia
documents:
  - server: Matrikon.OPC.Simulation.1
    tags:
      - id: Random.EIP.PLC01.QXR_RD1VRM01I02_MODE
        name: RD1_MD_VRM01_PID_MILL_FEED
        system: Raw Mill
        status: true      
      - id: Random.EIP.PLC01.QXR_RD1BI05A01W01
        name: RD1_PV_BI05_WEIGHT
        system: Raw Mill 
```

**Some important premises:**

- Each system must have its migration file like **kiln** and **raw_mill**.
- If the system is going to work with two or more OPC servers, there is no need to create separate migration files for 
these servers, group them on the same file. The structure above represents this well.
- The collector will not start if there are no tags.
 file. The MongoDB database must have been configured.

**Atention!** The database initialization script does not update the tag collection.

## Running
Create the collection `tags` on the database that will store
all the information about tags.

After that run the script execute`run_migrations.bat` to populate
the collection with the information from `*.yaml` file.
