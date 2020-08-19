from classes import Space
from db import db
from controllers import SpaceController
from views import RequestRTSDataView as rrdview, LocationViews as lview, SpaceView as Sview
from globals import START_PAGE_MESSAGE

collections = {"shows": db.tp_shows,
               "locations": db.location_collection}

def main():
    while True:
        ans = input(START_PAGE_MESSAGE)
        if ans == 'e':
            print("programme aborted")
            break
        elif ans == '1':
            rrdview.RequestRTSDataView()
        elif ans == '2':
            lview.LocationViews(collections).home_view()
        elif ans == '3':
            Sview.SpaceView(db.db).home_view()
            # SpaceController.CreateDataObject(collections)


if __name__ == "__main__":
    main()
