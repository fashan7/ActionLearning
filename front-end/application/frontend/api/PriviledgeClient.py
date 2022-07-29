import requests

from application.frontend.api.UrlClient import UrlClient


class PrivilegeClient:
    @staticmethod
    def read_url_one():
        obj = UrlClient()
        return obj.set_url_one()

    @staticmethod
    def group_sections(user_id):
        ob = PrivilegeClient.read_url_one()
        r = requests.get(f'{ob}api/get-section-postion/{user_id}')
        sections = r.json()
        return sections

    @staticmethod
    def get_sub_sections(user_id, section_id):
        ob = PrivilegeClient.read_url_one()
        r = requests.get(f'{ob}api/get-subsection/{user_id}/{section_id}')
        sub_sections = r.json()
        return sub_sections

    @staticmethod
    def get_primary_section():
        ob = PrivilegeClient.read_url_one()
        r = requests.get(f'{ob}api/primary-pages')
        return r.json()

    @staticmethod
    def get_priv_pages(section, user_id):
        ob = PrivilegeClient.read_url_one()
        r = requests.get(f'{ob}api/get-priv-pages/{section}/{user_id}')
        return r.json()

    @staticmethod
    def get_new_pages_not_set(section):
        ob = PrivilegeClient.read_url_one()
        r = requests.get(f'{ob}api/get-new-priv/{section}')
        return r.json()

    @staticmethod
    def post_insert_priv(page_id):
        ob = PrivilegeClient.read_url_one()
        r = requests.get(f'{ob}api/register-priv/{page_id}')
        return r.json()

    @staticmethod
    def update_page(id, status):
        ob = PrivilegeClient.read_url_one()
        r = requests.get(f'{ob}api/update-priv/{id}/{status}')
        return r.json()