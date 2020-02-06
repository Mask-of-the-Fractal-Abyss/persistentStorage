import json
import os.path

class StorageLocation:
    def __init__(self, path, debug=False, List=False):
        self.path = path
        self.debug = debug
        self.isList = List
        self.List = "[]" if List else "{}"
        if not os.path.isfile(self.path):
            if self.debug:
                print("File not found, creating file...")
            with open(self.path, "w") as f:
                f.write(self.List)
        else:
            if self.debug:
                print(">>Successfully found file.")
            try:
                self.getData()
            except json.decoder.JSONDecodeError:
                with open(self.path, "w") as f:
                    f.write(self.List)

    def clear(self):
        with open(self.path, "w") as f:
            f.write(self.List)

    def getString(self):
        with open(self.path, "r") as f:
            r = f.read()
            if self.debug:
                print("Read: ", r)
            return r
        raise FileNotFoundError

    def getData(self):
        return json.loads(self.getString())

    def write(self, data):
        if self.debug:
            print("Writing: ", data)
        with open(self.path, "w") as f:
            if type(data) is str:
                f.write(data)
            else:
                f.write(json.dumps(data))

    def store(self, key, data=None, append=True):
        if data is None:
            data = key
        j = self.getData()
        if type(j) is list:
            if self.debug:
                print(">>File contents are list type")
            if type(key) == int:
                j[key] = data
            elif key in j:
                if self.debug:
                    print("Data=", key, data, j.index(key))
                j[j.index(key)] = data
            else:
                if self.debug:
                    print("Appending: ", data)
                j.append(data)
        elif type(j) is dict:
            if self.debug:
                print(">>File contents are dict type")
            if key in j and type(j[key]) is list:
                if append:
                    j[key].append(data)
                else:
                    j[key] = data
            else:
                j[key] = data
        else:
            print("Json is neither list nor dict")
            raise TypeError
        self.write(j)

    def append(self, val):
        if self.debug:
            print("Appending...", val)
        if not self.isList:
            raise TypeError
        j = self.getData()
        j.append(val)
        self.write(j)

    def __getitem__(self, key):
        if self.debug:
            print("Getting...", key)
        d = self.getData()
        return d[key]

    def __setitem__(self, key, val):
        if self.debug:
            print("Setting...", key, val)
        self.store(key, val)
        
