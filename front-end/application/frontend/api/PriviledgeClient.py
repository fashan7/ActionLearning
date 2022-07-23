import requests

class PrivilegeClient:
    @staticmethod
    def group_sections():
        r = requests.get('http://127.0.0.1:5002/api/get-section-postion')
        sections = r.json()
        return sections

