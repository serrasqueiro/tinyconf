"""
Module that handles file packs, such as zip-files.

(c)2020  Henrique Moreira (part of 'tconfig')
"""


from zipfile import ZipFile
from yadate import *


#
# CLASS GenFile (abstract)
#
class GenFile():
    def init_genfile (self, name, aStat, nick=None):
        self.pathName, self.nick = name, nick
        if name is not None: self.set_name( name )
        self.payload = (None, "")
        self.lastCRC = -1
        self.lastEncoding = None


    def set_name (self, name):
        assert type( name )==str
        self.pathName = name
        aName = name.lower()
        if aName.endswith(".zip"):
            kind = "zip"
        else:
            kind = "text"
        self.kind = kind


    def calc_mini_crc (self, skipCR=False):
        textualHint, data = self.payload
        assert data is not None
        v = 0
        if textualHint=="txt":
            for c in data:
                if skipCR and c=="\r": continue
                v = (v + ord(c)) % 65537
        elif textualHint=="bin":
            for c in data:
                if skipCR and chr(c)=="\r": continue
                v = (v + c) % 65537
        else:
            assert False
        self.lastCRC = (textualHint, v)
        return v


#
# CLASS ATextFile
#
class ATextFile(GenFile):
    def __init__ (self, name, nick=None, autoOpen=True):
        self.init_genfile( name, None, nick )


    def raw_read (self):
        self.lastEncoding = "bin"
        with open( self.pathName, "r" ) as fp:
            self.payload = ("txt", fp.read())
        return True


    def text_read (self):
        self.lastEncoding = None
        for anEncoding in ("ascii",
                           "UTF-8",
                           "ISO-8859-1",
                           ):
            try:
                with open( self.pathName, "r", encoding=anEncoding ) as fp:
                    data = fp.read()
            except:
                data = None
            if data is not None:
                self.payload = ("txt", data)
                self.lastEncoding = anEncoding
                return anEncoding
        return ""


#
# CLASS FilePack
#
class FilePack(GenFile):
    def __init__ (self, name, aStat=None, nick=None, autoOpen=True):
        self.init_genfile( name, aStat, nick )
        self.subs, self.zipFileList, self.orderedList = [], [], []
        self.magic = dict()  # simple magic info, or any kind of CRC
        self.isZip = False
        if autoOpen:
            self._open_file( self.kind )


    def _open_file (self, aKind):
        if aKind=="zip":
            self.isZip = True
            z = ZipFile( self.pathName )
            self._update_from_zipinfo(z.namelist(), z.filelist, z)
        else:
            z = open(self.name, "rb")
        self.handler = z
        return True


    def simple_content (self, subName=None, basicText=None):
        assert basicText in (None, "a",)
        # 'a' means mostly text (ignore CR)
        if self.isZip:
            assert subName is not None
            if basicText is None:
                with self.handler.open(subName, "r") as fp:
                    data = fp.read()
                try:
                    textual = data.decode("utf-8")
                except:
                    textual = None
                if textual is None:
                    self.payload = ("bin", data)
                else:
                    s = textual.replace("\r", "")
                    self.payload = ("txt", s)
            elif basicText is "a":
                with self.handler.open(subName, "r") as fp:
                    data = fp.read()
                textual = data.decode("ascii")
                s = textual.replace("\r", "")
                self.payload = ("txt", s)
        else:
            data = self.handler.read()
            self.payload = ("bin", data)
        miniCRC = self.calc_mini_crc()
        self.magic[ subName ] = miniCRC
        return miniCRC


    def _update_from_zipinfo (self, nameList, fileList, z=None):
        self.subs, self.zipFileList, self.orderedList = nameList, fileList, []
        sOrder = []
        for elem in fileList:
            yDate = GenFDate( elem.date_time )
            s = "{} {}".format( yDate, elem.filename )
            sOrder.append( s )
        sOrder.sort()
        self.orderedList = sOrder
        return True


#
# Main script
#
if __name__ == "__main__":
    print("Import this module. Running this script does not do anything.")
