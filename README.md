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
