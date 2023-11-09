# challenge-api

Challenge api

# Project structure
```
challenge-api/
├─ app.py
├─ README.md
├─ Dockerfile
├─ config.properties.template
├─ src/
│  ├─ service/
│  ├─ utils/
├─ test/
│  ├─ service/
│  ├─ utils/
│
```


## Summary

1. [setup the environment and run the application](#setup-the-environment-and-run-the-application)
   - [steps](#steps)
   - [steps details](#steps-details)
     - [postgres instalation steps](#postgres-instalation-steps)
     - [create the depency table](#create-the-depency-table)
     - [set up the config.properties file](#set-up-the-config.properties-file)
     - [execute automated test](#execute-automated-test)
     - [execute test coverage](#execute-test-coverage)
1. [API documentation](#api-documentation)
1. [few help and references used](#few-help-and-references-used)


## setup the environment and run the application


### steps

1. [install](https://docs.docker.com/engine/install/) docker 
1. Clone the repository
   - `git clone --single-branch --branch docker_version git@github.com:zioli/challenge-api.git`
1. Pull and execution of the Postgres Docker image(see [postgres Docker image pull and execution](#postgres-Docker-image-pull-and-execution))
1. create the dependency table (see [create the depency table](#create-the-depency-table))
1. set up the `config.properties` file  (see [set up the config.properties file](#set-up-the-config.properties-file))
1. Create the repository Docker image (see [Create the repository Docker image](#create-the-repository-docker-image))
1. Execute the repository Docker image (see [Create the repository Docker image](#execute-the-repository-docker-image))
1. Automated test execution (see [execute automated test](#execute-automated-test))
1. Test coverage execution (see [execute test coverage](#execute-test-coverage))

### steps details

#### postgres Docker image pull and execution

- Get the postgres image by executing 

```
docker pull postgres
```

- Start the container by executing 

```
docker run -it \
    --name postgres_container \
    -e POSTGRES_USER="<user>" \
    -e POSTGRES_PASSWORD="<password>" \
    -e POSTGRES_DB="<database>" \
    -d \
    -p 5432:5432 \
    postgres
```

> **where**
>
> &nbsp;&nbsp;&nbsp;**password**: The `password` that will be used to access the database
> 
> &nbsp;&nbsp;&nbsp;**user**: The `user` that will be used to access the database
> 
> &nbsp;&nbsp;&nbsp;**database**: The `database name` that will be created on postgres start

#### create the depency table
- Once you complete the steps above, then you have to access the posgres database container. Execute the follow command:

```
docker exec -it <cointainer_id> bash
```

> **where**:<BR>
>
> &nbsp;&nbsp;&nbsp;**cointainer_id**: Is the  `cointainer id` returned when the `docker run` command was executed

When  redirected to the container terminal, then execute:

```
psql postgresql://<user>:<password>@localhost:5432/postgres
```

There we go, now you are able to create the table that will be used as example:

``` sql
CREATE TABLE cars (
  brand VARCHAR(255),
  model VARCHAR(255),
  year INT
);
```

this example was taken from [w3school](https://www.w3schools.com/postgresql/postgresql_create_table.php)

#### set up the config.properties file

create or modify the `config.properties` file. It is located at the project root folder


for convenience, it was added to the project the file `config.properties.template`. It can be renamed to `config.properties` and changed as convenient.

or you can create a new file, copy and past the content bellow and modify the variables as convenient
```
[postgres]
database.dbname=<postgres database>
database.user=<postgres user>
database.password=<postgres password>
host=localhost
port=5432
load.lines_limit=1000

[logging]
name=challenge
```
> **where**:<BR>
>
> &nbsp;&nbsp;&nbsp;**database.dbname**: The same `database` name used when the postgres container was started<sup>*</sup>
>
> &nbsp;&nbsp;&nbsp;**database.user**: The same `user` name used when the postgres container was started<sup>*</sup>
>
> &nbsp;&nbsp;&nbsp;**database.user**: The same `password` used when the postgres container was started<sup>*</sup>
>
> &nbsp;&nbsp;&nbsp;**host**: The `host` can be changed, but for testing we recomend use the value set
>
> &nbsp;&nbsp;&nbsp;**port**: The `port` can be changed, but for testing we recomend use the value set
>
> &nbsp;&nbsp;&nbsp;**load.lines_limit**: The `load.lines_limit` can be changed, but it was keep as 1000 due the challenge requirements 

<sup>* see [postgres instalation steps](#postgres-instalation-steps) for more details</sup>

#### Create the repository Docker image

```
docker run -it \
    --name postgres_container \
    --expose="5432" \
    -e POSTGRES_USER="<user>" \
    -e POSTGRES_PASSWORD="<password>" \
    -e POSTGRES_DB="<database>" \
    -d \
    -p 5432:5432 \
    postgres
```
> **where**:<BR>
>
> &nbsp;&nbsp;&nbsp;**<user>**: The same `user` name used when the postgres container was started<sup>*</sup>
>
> &nbsp;&nbsp;&nbsp;**<password>**: The same `password` used when the postgres container was started<sup>*</sup>
>
> &nbsp;&nbsp;&nbsp;**<database>**: The same `database` name used when the postgres container was started<sup>*</sup>
>

#### Execute the repository Docker image

```
docker run -it \
    --name flask_container \
    -d \
    -p 8000:8000 \
    flask_docker
```


#### execute automated test

```
python -m pytest -v -s
```

#### execute test coverage

```
python -m pytest -v -s --cov
```


## API documentation

#### Uploading historic data to a table

<details>
<summary><code>GET</code> <code><b>/migration/load/historic/{source}/{database}/{table}</b></code> (upload a given file or content to a database.table on postgres. <BR> The api will be available under <code>http://localhost:8000/</code></summary>

##### Parameters

| name      |  type     | data type               | default | description                                                           |
|-----------|-----------|-------------------------|---------|-----------------------------------------------------------------------|
| source    | required  | string                  |         | The data source, that means where the data is actually store, currently it has 4 partial implementation `aws` `gcp` `content` `test` <BR>`aws` it load file from s3 into postgress (not implemented yet)<BR>`gcp` it load file from GCP Storage into postgress (not implemented yet)<BR>`content` it load the body csv content into postgress (**implemented**)<BR>`test` it examplify how to convert the `s3`/`gcp storage` into a `FileStorage` and load into postgre (**implemented**)|
| database  | required  | string                  |         | The datasource where the postgres table will be find|
| table     | required  | string                  |         | The target table name where the data will be loaded|
| header    |           | string                  |true     | it indicates if the file to be loaded contains header. If none of the following values are informed, it will be set as `true`: (case insensitive) `false`|`no`|`not`|`0` 


##### body
| name      |  type     | data type               | default | description                                                           |
|-----------|-----------|-------------------------|---------|-----------------------------------------------------------------------|
| file      | *required | string                  |         | It is the csv file content that will be send as part of the Body form-data file on the request. <BR>*required* if `source` is set as `content`. <BR> *see [Upload a file via POST request](https://www.postman.com/postman/workspace/postman-answers/documentation/13455110-00378d5c-5b08-4813-98da-bc47a2e6021d) for more details*|


</details>


## few help and references used

Probably we got more references and help but also it is likely it was forget..sorry about that

https://stackoverflow.com/questions/20015550/read-file-data-without-saving-it-in-flask

https://tedboy.github.io/flask/interface_api.incoming_request_data.html#flask.Request.files

https://hub.docker.com/_/postgres

https://stackoverflow.com/questions/37694987/connecting-to-postgresql-in-a-docker-container-from-outside

https://huzaima.io/blog/connect-localhost-docker

https://www.mend.io/free-developer-tools/blog/docker-expose-port/

https://medium.com/geekculture/how-to-dockerize-your-flask-application-2d0487ecefb8

https://docs.pytest.org/en/6.2.x/fixture.html

https://gist.github.com/azagniotov/a4b16faf0febd12efbc6c3d7370383a6#creating-newoverwriting-existing-stubs--proxy-configs

https://tedboy.github.io/flask/interface_api.incoming_request_data.html#flask.Request.files



