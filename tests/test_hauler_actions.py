import json

import pytest
from Endpoints.tickets import Tickets
from Endpoints.Impersonate import impersonate as I
from Helpers.file_opener import FileOpener as FO
from Helpers.db_helper import DBHelper as DB

class TestHaulerActions():


    @pytest.mark.imp
    def test_impersonate(self,base_url,default_headers):
        file = {
            "HaulerId": 7
        }
        person = I.Impersonate.impersonate_hauler(base_url=base_url,default_headers=default_headers,
                                                  file=file)

        print(person)