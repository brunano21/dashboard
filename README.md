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

From `<project root folder>/server` run the server,

	python server.py

Access to the application at

	http://127.0.0.1:5000/

The generator is a script that randomly creates and posts data to the server in order to emulate user's download. To run the generator, open a new terminal, from `<project root folder>/generator` folder run:

	python generator.py

In order to run tests, from `<project root folder>/server/tests` run

	python test.py
