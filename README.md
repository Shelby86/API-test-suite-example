# Gemini-API-Tests


Hello and welcome to the Gemini API automation

Set Up:

- To run these tests, in the conftest.py file, change the username after the return

To run a test by marker: python3 -m pytest -m mark_name

To run with print statements:

pytest -m marker --log-cli-level=DEBUG -s

or as a whole

pytest --log-cli-level=DEBUG -s