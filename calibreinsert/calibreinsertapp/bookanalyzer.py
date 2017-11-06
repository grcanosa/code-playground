"""
Book analyzer
"""

import zipfile
from lxml import etree

class BookAnalyzer:
    def __init__(self):
        self.filepath=None
        self.title = None
        self.author = None

    def analyze(self,filepath):
        print("lalala")
    def get_epub_info(self,fname):
        ns = {
            'n':'urn:oasis:names:tc:opendocument:xmlns:container',
            'pkg':'http://www.idpf.org/2007/opf',
            'dc':'http://purl.org/dc/elements/1.1/'
        }

        # prepare to read from the .epub file
        zip = zipfile.ZipFile(fname)

        # find the contents metafile
        txt = zip.read('META-INF/container.xml')
        tree = etree.fromstring(txt)
        cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]

        # grab the metadata block from the contents metafile
        cf = zip.read(cfname)
        tree = etree.fromstring(cf)
        p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]
        print(p)
        # repackage the data
        res = {}
        for s in ['title','language','creator','date','identifier']:
            res[s] = p.xpath('dc:%s/text()'%(s),namespaces=ns)[0]

        return res
