import json

from requests import session
sess = session()

class Impersonate():


    def impersonate_hauler(base_url,default_headers,file):
        req = sess.post(url=f'{base_url}/auth/impersonate',headers=default_headers,
                        data=json.dumps(file))

        res = req.text

        return res