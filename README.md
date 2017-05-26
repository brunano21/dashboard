In order to run this, make sure you have installed:
- bower
- python v2.7

Then follow the below steps:

Install virtualenv

    sudo pip install virtualenv
Clone the repository

	git clone https://github.com/brunano21/dashboard

Move into newly created `dashboard` folder

	cd dashboard

Create a virtual environment

	virtualenv venv

Activate the virtual environment

	. venv/bin/activate

Install project's dependencies (python's and bower's)

	pip install -r requirements.txt
	cd server && bower install && cd ..

Tell Flask where your main application lives

	export FLASK_APP=server/server.py

Run the server

	flask run

Access to the application

	http://127.0.0.1:5000/

In order to run the generator, open a new terminal, into the `<project root folder>/generator` and run:

	python generator.py
