## Petroleum Statistics

A mini project that shows [add_description](:-)

## Getting Started

1. Rename .env.example to .env and setup variables
2. If you have docker installed, then just run `docker-compose up --build`, which
   runs spins up the django server available http://localhost:8080

3. If you don't have docker installed, then follow these to setup the server:
   $ python -m venvvenv
   $ source venv/bin/activate # on bash or,
   $ .\venv\Scripts\activate.bat # on powershell/cmd
   $ python -m pip install -r requirements.txt
   $ python manage.py seed_db # to load required data on database
   $ python manage.py runserver # to run django server on http://localhost:8000

## Testing app

To run the tests, run:
$ python manage.py test

## Todos

- [x] Implement cli for database seed/reset
- [x] Add a way to use from cli
- [ ] Implement api and api keys for consumers to use api
- [ ] Think and implement more...

## deployment

I'm using fly.io for deployment. To deploy it on fly.io just run:
$ fly
