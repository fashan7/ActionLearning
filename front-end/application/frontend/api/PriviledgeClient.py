import requests

class PrivilegeClient:
    @staticmethod
    def group_sections(user_id):
        r = requests.get(f'http://127.0.0.1:5002/api/get-section-postion/{user_id}')
        sections = r.json()
        return sections

    @staticmethod
    def get_sub_sections(user_id, section_id):
        r = requests.get(f'http://127.0.0.1:5002/api/get-subsection/{user_id}/{section_id}')
        sub_sections = r.json()
        return sub_sections

