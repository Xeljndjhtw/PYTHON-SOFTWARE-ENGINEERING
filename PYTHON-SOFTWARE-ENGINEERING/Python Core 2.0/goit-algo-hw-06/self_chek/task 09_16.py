from collections import UserDict


class LookUpKeyDict(UserDict):
    def lookup_key(self, value):

        keys = []
        for key in self:
            if self[key] == value:
                keys.append(key)
        return keys