from Endpoints.facilities import Facilities
from Helpers.file_opener import FileOpener as FO
import pytest

class TestFacility:


    @pytest.mark.facility_ticket
    def test_create_facility_ticket(self,base_url,default_headers):

        file = FO.open_json_file(file_name='Data/facilities.json')

        ticket = Facilities.create_facilities_ticket(base_url,default_headers,file=file)

        print(ticket)