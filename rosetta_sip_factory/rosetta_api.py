import mechanicalsoup as mechanize
from suds.client import Client

from pds import grab_pds


class DepositAPI:

    def __init__(
            self, username, password, institute,
            deposit_url="http://127.0.0.1",
            pds_url="http://127.0.0.1"):
        self.username = username
        self.password = password
        self.institute = institute
        self.deposit_url = deposit_url
        self.pds_url = pds_url

    def submit_deposit_activity(
            self, material_flow_id, sub_directory, 
            producer_id, deposit_set_id):
        pds = grab_pds(self.username, self.password,
                       self.institute,self.pds_url)
        deposit_client = Client(self.deposit_url)
        ws_call = deposit_client.service.submitDepositActivity(
                    pds, material_flow_id, sub_directory,
                    producer_id, deposit_set_id)
        return ws_call
