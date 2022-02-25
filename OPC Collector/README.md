# OPC Data Collector

This application is intended to collect data from OPC Server and save it in MongoDB.

## System Requirements

 - Windows 7/8/10

 - [Python 3.8.3](https://www.python.org/downloads/release/python-383/) **x86** *(Due to limitations in the OPC library)*
 - [MongoDB](https://www.mongodb.com/)
 - [Mongo Compass](https://www.mongodb.com/products/compass) *(Optional)*

## Installing virtual environment

- ### Automatic Installation

To install the virtual environment goes to opc-collector folder
and run `install.bat` script.
```bash
>.\install.bat
```
The script will search for python 3.8.3-32 bits installation and
will create a virtual environment with required libs.

First, make sure you are inside a [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html). You can install dependencies in the Python local environment if you prefer, but doing so is highly discouraged.
**If you prefer not to use a virtual environment, you must change the `run_collector.bat` file.**

Before:

````bash
echo Activating the virtual environment...
call .\venv\Scripts\activate.bat
echo Installing dependencies...
call pip install --no-index --find-links=dependencies -r .\requirements.txt
call .\venv\Scripts\deactivate.bat
````

After:

````bash
echo Installing dependencies...
call pip install --no-index --find-links=dependencies -r .\requirements.txt
call .\venv\Scripts\deactivate.bat

````

- ### Manual Installation (Skip this part if you performed the automatic installation)

Run:

If you have more then one version installed:

````bash
py -3.8 -m venv virtual_env
````

If you have just the required version:
````bash
python -m venv virtual_env
````

After you create the virtual environment, you nedd to activate it. 

````bash
.\virtual_env\Scripts\activate.bat
````

After activation, install the dependencies manually with the command `pip install package_name`.

Example:

````bash
pip install six-1.15.0-py2.py3-none-any.whl 
````

**All dependencies are in the `dependencies` folder.**

## Collector set up

The collector can work with N databases, you can add a new connection configuration in the `config.yaml` file
in the `opc-collector` folder.

- ### MongoDB

````yaml
  databases:
  - db_name: "DATABASE NAME"
    db_host: 127.0.0.1
    db_port: 27017
    db_user: "DATABASE USER"
    db_pass: "DATABASE PASSWORD"
````


- ### Collector

````yaml
collector:
  max_reading_attempts: 5
  max_connect_attempts: 3
  max_interval_reading: 30
````

- **max_reading_attempts**: Number of reading attempts.
- **max_connect_attempts**: Number of connection attempts.
- **max_interval_reading**: Interval in seconds between each reading. It will be the same for all servers.

## Database initialization

See `db-config` project.

## How it works

![Diagram](https://i.imgur.com/6MFkE8u.png)

## Starting

To start the collector, just run `run_collector.bat`.

```bash
>.\run_collector.bat
```

## Stopping

To stop the collector, just run `stop_collector.bat`.

```bash
>.\stop_collector.bat
```