import pytest
from Endpoints.tickets import Tickets
from Helpers.file_opener import FileOpener as FO

file = FO.open_file(file_name='tests/Data/ticket.json')
print(file)