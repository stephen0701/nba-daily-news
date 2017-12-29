import leveldb

# converting functions
def cvt_to_bytes(string):
    # leave type check for system exceptions
    return string.encode('ascii')


def cvt_to_string(bytestring):
    # leave type check for system exceptions
    return bytestring.decode('utf-8')


def cvt_b(key, value):
    key_b = key
    value_b = value
    if isinstance(key, type('str')):
        key_b = cvt_to_bytes(key)
    if isinstance(value, type('str')):
        value_b = cvt_to_bytes(value)
    return key_b, value_b


def cvt_s(key, value):
    key_s = key
    value_s = value
    if isinstance(key, type(b'bytes')):
        key_s = cvt_to_string(key)
    if isinstance(value, type(b'bytes')):
        value_s = cvt_to_string(value)
    return key_s, value_s


# database functions
def init(filename):
    db = leveldb.LevelDB(filename)
    return db


def insert(db, key, value):
    key_b, name_b = cvt_b(key, value)
    db.Put(key_b, name_b)


def delete(db, key):
    key_b = cvt_to_bytes(key)
    db.Delete(key_b)


def update(db, key, value):
    key_b, name_b = cvt_b(key, value)
    db.Put(key_b, name_b)


def search(db, key):
    key_b = cvt_to_bytes(key)
    value = db.Get(key_b)
    value_str = cvt_to_string(value)
    return value_str

def isValid(db, key):
    try:
        key_b = cvt_to_bytes(key)
        value = db.Get(key_b)
        if value:
            return True
        else:
            print("The value is NULL.")
            return False
    except KeyError:
        return False
    else:
        print("Unknown Error.")
        return False
    
def get_keys(db):
    lst_keys = list()
    for key in db.RangeIter(include_value = False):
        key_s = cvt_to_string(key)
        lst_keys.append(key_s)
    return lst_keys
    
def dump(db):
    for key, value in db.RangeIter():
        key_s, value_s = cvt_s(key, value)
        print (key_s, value_s)