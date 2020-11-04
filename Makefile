.SILENT: default

default:
	echo "Available commands :"
	echo "\t + 'make install': create and install virtualenv"
	echo "\t + 'make run': start the game"

run:
	./venv/bin/python3 main.py

install: venv install_pip

venv:
	virtualenv venv --python=python3

install_pip:
	./venv/bin/pip install -r ./requirements.txt
