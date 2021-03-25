[![foodgram](https://github.com/IvanDeveloperPro/foodgram-project/workflows/foodgram/badge.svg)](https://github.com/IvanDeveloperPro/foodgram-project/actions)

# Foodgram
The example this project id deploying on the IP 84.201.164.21. 

The project represent itself a recipes blog. You could save recipe, watch recipes others users, follow to users liked you recipe, download list ingredients for preparing recipes and others...

## Getting Started
For deploing project you need copy from repository on your local or remote server.

### Prerequisites
You need install Docker and docker-compose. The download link: https://docs.docker.com/

```
sudo apt install docker
```
### Installing

For start project you need exec command
```
sudo docker-compose up -d
```
After starting and running docker container
```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py loaddata data.json
```
The django applying all need migrations

For access to admin panel need create superuser
write command below and further filling all requirement fields 
```
sudo docker-compose exec web python manage.py createsuperuser
```

## Authors
@IvanDeveloperPro 


## License
This project is licensed under the MIT License - see the LICENSE.md file for details
