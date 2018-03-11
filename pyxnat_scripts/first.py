import os

from pyxnat import Interface
from xml.dom import minidom

cnc = Interface(server='http://192.168.10.17:8080', user='python', password='', cachedir='/tmp')

projects = cnc.select.projects().get()


subjects = cnc.select.projects('*').subjects()

for s in subjects:

    experiments = s.experiments()
    for e in experiments:
        dicoms = e.scans()
        for d in dicoms:
            str = d.get()
            xml = minidom.parseString(str)

            elm = xml.getElementsByTagName("xnat:MRScan")

            #scantype = elm[0].attributes["type"].value

            #if scantype == 'MPRAGE':
            os.mkdir('/data/xnat/tmp/cnc_converter')
            dicoms.download('/data/xnat/tmp/cnc_converter/', type='ALL', extract=False)

        
    
    
