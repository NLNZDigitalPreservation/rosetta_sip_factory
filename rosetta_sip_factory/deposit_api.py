import mechanicalsoup as mechanize
from suds.client import Client

from pds import grab_pds


class DepositAPI:

    def __init__(self, 
            username, 
            password, 
            institute,
            deposit_url="http://127.0.0.1",
            pds_url="http://127.0.0.1"):
        self.username = username
        self.password = password
        self.institute = institute
        self.deposit_url = deposit_url
        self.pds_url = pds_url

    def submit_deposit_activity(self, 
            producer_id, material_flow_id, sub_directory):
        pds = grab_pds(self.username, self.password, self.institute, self.pds_url)
        print(pds)


def main():
    d_api = DepositAPI("serverside", "ServerSide1234", "INS00",
        "http://slbdpstest.natlib.govt.nz/dpsws/deposit/DepositWebServices?wsdl",
        "http://slbpdstest.natlib.govt.nz/pds?func=load-login&url=http://slbpdstest.natlib.govt.nz/pds")
    d_api.submit_deposit_activity("111", "111", "subdir")

if __name__ == '__main__':
    main()