"""
Yet another ordered dictionary!

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-function-docstring, too-few-public-methods, no-self-use


#
# Abstract CLASS DGeneric
#
class DGeneric():
    """
    DGeneric, a generic dictionary abstract class
    """
    def init_dgeneric(self, a_desc):
        assert isinstance(a_desc, str)


#
# CLASS DOrder
#
class DOrder(DGeneric):
    """
    Dictionary Order, simplified class
    """
    def __init__(self, data=None, a_desc=""):
        self.init_dgeneric(a_desc)
        self.desc = a_desc
        self.data, self.keying = self._set_from_dict(data)


    def _set_from_dict(self, data):
        if data is None:
            return dict(), []
        keys = list(data.keys())
        keys.sort()
        return data, keys


    def get_keys(self):
        """
        Get dictionary keys, as a list
        :return: list
        """
        return self.keying


#
# CLASS

#
# Main script
#
if __name__ == "__main__":
    print("""Import this module.
""")
