from globals import *
from ssr_rts_api import Client as Cl
from db import db
import time

credentials = {"username": "Your credentials",
               "password": "Your password"}
querystring = {
    "query": "'id'='103'",
    "rows": 0,
    "start": 0,
    "minPublicationDate": 1960,
    "maxPublicationDate": 2020,
    "sort": "publicationDate"
}


class RequestRTSDataView:

    """
    request rts api view
    use the ssr_rt_api package
    """

    def __init__(self):
        self.view()
        self.docs = int()

    def view(self):

        document_array = list()
        counter = 0

        while True:
            print(RESQUEST_DATA_VIEW_WELCOME_STR)
            ans = input('Value : ')
            if ans == 'e':
                break
            elif ans == '2':

                show_collection = db.db['tp_show_lite']

                save_ans = input('############################################\n'
                                 'WARNING : data in collection will be dropped\n'
                                 '############################################\n'
                                 'save data ? y/n : ')
                if save_ans == 'n':
                    break
                else:
                    show_collection.drop()
                    # test with TEST_DATA_SET g var
                    Cl.Client.save_data(document_array, show_collection)

            elif ans == '1':
                client = Cl.Client(credentials)
                print("\nclient ready")
                ans_req = input("run request ? y/n (default y): ")
                if ans_req == 'n':
                    break
                else:
                    print("wait...")
                    client.request(querystring)
                    self.docs = client.document_count
                    doc_count = client.document_count

                    while counter < doc_count:
                        querystring['start'] = counter
                        querystring['query'] = "'id'='103'"
                        res = client.request(querystring)
                        res = res.json()

                        # add filter here

                        data_filtered = client.filter_data(res['data'], ['program', 'id'], '103')
                        swiss_productions = [doc for doc in data_filtered if 'mediaURL' in doc]

                        document_array += swiss_productions

                        counter += 25
                        time.sleep(0.10)

                    print("request over collection got {} documents".format(len(document_array)))
