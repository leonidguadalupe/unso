# UNSO
Unsō(運送, which stands for "shipping") is a python app used to show shipping prices between different ports around the world.

## Installation
First step is to make sure that you have docker installed in your system. Visit [Docker](https://docs.docker.com/engine/install/) to check if your current platform supports it.

We can also assume that you have Git installed in your system. Let's just make sure you have it with this.
```bash
git version
```
If it outputs a version, then we're good to go.

Now, time to get the repository. Clone this repository:
```bash
git clone https://github.com/leonidguadalupe/unso.git unso
cd unso
```

#### ENV FILE
Make an .env file as well and make sure you have similar info with the env file you will be making. 

Here's an example of a .env file that you need to have setup in the root directory of your project:
```bash
POSTGRES_USER=xeneta
POSTGRES_PASSWORD=WH38R5mTjeeaAQd6 (use a password generator)
POSTGRES_DB=postgresdb
POSTGRES_DB_HOST=db
FLASK_APP=source.py
EXCHANGE_RATE_APP_ID=953aabb1f47e43419119fbb74db97fda
```
#### Create Volumes
After adding all those information, we need to build the docker-compose yaml file. You need to create the docker volumes first though so do:
```bash
docker volume create postgres_data
```
#### Build images using the compose file
Then start building the images from the compose file. Do it by entering:
```bash
docker-compose -f docker/docker-compose.yml build
```
#### Run containers
After build, you can now launch the containers for your app.
```bash
docker-compose -f docker/docker-compose.yml up
```

You need to login to the unso container with the flask app to migrate your database.
```bash
docker exec -it unso sh
cd main
flask db upgrade
```
#### Add fixture data to database
run this docker command to put add fixtures to db
docker exec -i unsodb psql -U xeneta postgresdb < rates.sql 

### Price get & post API
This is how you form your POST request. In the body of the request, you need these keys.
"currency" parameter is optional and you should use a proper currency code to enable sending
to 
```json
{
  "date_to": "2020-02-22",
  "date_from": "2020-02-22",
  "price": 5678,
  "origin": "CNGGZ",
  "currency": "AED",
  "destination": "BEANR"
}
```
And you will be sending that post request to this endpoint:
http://localhost:8000/prices

For the get requests, it will remain the same as how things are designed in the test itself.


## BATCH Processing question
To perform batch processing, there are some things that we would need to consider:
1. How often do we need to move data?
2. What protocol is the data accessible with?
3. If #2 answer is not a protocol, hence a file of some sort, is there a way to automate the downloading of that file in a particular location?

My thought process for this is we need to determine first where the data comes from. Then, if we need to run it more than once a day, it would be great if we could use Celery to create a task to run the code or the script that fetches data from the source and finally add a heartbeat to perform polling. Ideally, it can also be used to automate the downloading of the file from a cdn by any case it is not available via http, ssh or soap. If the source is a database, we can check when the data is updated (if that "updated" column is available), and in every sync we do, we store that value somewhere so we dont have to redownload data that hasnt changed during that period by filtering through that datetime object. Also, to speed up the creation of data, we can create a virtual tsv file, put the contents of the fetched data from source in there and do a postgres "copy from" that simply compies from the virtual store towards our database (I have benchmarked this approach a couple of times and it's the fastest if you want to move millions of data).

Another approach for me (with a capable team, the right environment and a good budget) is we can deploy Kafka connectors to the sources and install [Debezium](https://debezium.io/documentation/reference/index.html) in our environment. This approach checks for any changes in the database source and then records those changes in the stream which we can respond from as consumers. Every change logged will be moved in our databases so it will not incur heavy computing operation on the source side (dumping millions of data for example)