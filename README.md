# Maxwell Casa
**A web development project combining Flask, Docker, Raspberry Pi, and a lot of sheep**
## What it's for
It serves as a central repository for different side projects (Raspberry Pi applications, web apps, games, blogs, etc.). Right now some of these are included in this repo but in the future this will be just the entrypoint with different groups of side projects running as stand-alone services.

---
## Running the application locally
### Pre-requisites
1. docker-machine
2. docker-compose
3. a `.env` file with all your passwords (a sample one is included with the public repo)

### Starting the web server
1. clone the repo
2. use docker-machine to host the environment in a VM (here's a great tutorial on how)
3. Once ssh'd into the docker-machine, run `startup.sh` to build the docker containers, start the web server and build the database

The application should now be running on your docker-machine's IP address.
---
## TODO
* move each "tile" to a stand-alone service hosted on its own subdomain
* give users different permissions to different applications
* develop a strategy for managing caching, persistence, and screen size. Probably something resembling a PWA


## credits
* much of the structure of this application was learned from [this tutorial](https://realpython.com/blog/python/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/)
* The domains were purchased through Squarespace. Seriously, what a great company!