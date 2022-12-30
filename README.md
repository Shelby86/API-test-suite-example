# Gemini-API-Tests


Hello and welcome to the Gemini API automation

Set Up:

- To run these tests, in the conftest.py file, change the username after the return

To run a test by marker: cd to the tests directory, then python3 -m pytest -m mark_name -s

To run with print statements:

pytest -m marker --log-cli-level=DEBUG -s

or as a whole

pytest --log-cli-level=DEBUG -s

or simply pytest -s

to install the requirements:

pip3 -r requirements.txt