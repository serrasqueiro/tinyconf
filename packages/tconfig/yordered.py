"""
Yet another ordered directionary!

(c)2020  Henrique Moreira (part of 'tconfig')
"""


#
# CLASS DGeneric
#
class DGeneric():
    def init_dgeneric (self, desc):
        assert type( desc )==str
        self.desc = desc


#
# CLASS DOrder
#
class DOrder(DGeneric):
    def __init__ (self, data=None, desc=""):
        self.init_dgeneric( desc )
        self.data, self.keying = self._set_from_dict( data )


    def _set_from_dict (self, data):
        if data is None: return dict(), []
        keys = list( data.keys() )
        keys.sort()
        return data, keys

#
# Main script
#
if __name__ == "__main__":
    print("""Import this module.
""")
