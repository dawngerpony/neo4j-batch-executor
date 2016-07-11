SHELL := /bin/bash

install:
	pip install -r requirements.txt

run:
	python -m py_compile add_uuids.py
	python add_uuids.py

# from http://blog.bottlepy.org/2012/07/16/virtualenv-and-makefiles.html

# Makefile
venv: venv/bin/activate
venv/bin/activate: requirements.txt
    test -d venv || virtualenv venv
    venv/bin/pip install -Ur requirements.txt
    touch venv/bin/activate

devbuild: venv
    venv/bin/python setup.py install

test: devbuild
    venv/bin/python test/runtests.py

