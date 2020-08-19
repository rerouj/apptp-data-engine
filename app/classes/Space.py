from bson import ObjectId


class Space(object):

    """space classes"""

    def __init__(self, show, show_title, space):
        self._id = ObjectId()
        self.show = show  # store tp_shows ObjectIds
        self.show_title = show_title
        self.space = space  # store location_collection ObjectIds
        self.locality_space = list()
        self.region_space = list()
        self.country_space = list()
        self.locations_name = list()
        self.distance = dict()  # store total dist between location

    def __str__(self):
        str1 = "Space ID : {}".format(self._id)
        str2 = "Show ID : {}".format(self.show)
        str3 = "Show Title : {}".format(self.show_title)
        str4 = "Number of location in space {}".format(self.freq_space())
        str5 = "Locations : {}".format(self.locations_name)
        return "\n{}\n{}\n{}\n{}\n{}".format(str1, str2, str3, str4, str5)

    def freq_space(self):
        return len(self.space)

    def get_id(self):
        return self._id

    def get_space(self):
        return self.space

    def show_space(self):
        print(self.space)

"""
space = Space()
space._show = 'hello'

schema = SpaceSchema()
result = schema.dump(space)
print(result)


    test_object1 = Space('hello')
    test_object2 = Space('ca va')
    test_object3 = Space('bien ?')
    
    db = [test_object1, test_object2, test_object3]
    
    with open("pickles/test.db", 'wb') as file:
        pickle.dump(db, file)
    
    with open("pickles/test.db", 'rb') as db_file:
        db = pickle.load(db_file)
    
    for i in db:
        print(i.name)
"""