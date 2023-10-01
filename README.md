# bookman
[![Docker Pulls](https://badgen.net/docker/pulls/acetheking987/bookman?icon=docker&label=pulls)](https://hub.docker.com/r/acetheking987/bookman)

automatically query and download books from google and ao3. frontend comming soon

## docker useage
example docker compose usage
```
services:
    mongo:
        image: mongo
        volumes:
            - data:/data/db
        
    bookman:
        container_name: bookman
        image: bookman
        ports:
            - 27018:27018
        links:
            - mongo
        environment:
            - GOOGLE_API_KEY=your google api key
            - AO3_USERNAME=your ao3 username (optional)
            - AO3_PASSWORD=your ao3 password (optional)
            - MONGODB_URI=mongodb://mongo:27017
            - AUTO_SAVE_QUERY=true
volumes:
    data:
```
