import os
import pickle
import logging

from pyxnat import Interface
from xml.dom import minidom


class CNC_Converter(object):
    
    def __init__(self):

        self.interface = Interface(server='http://192.168.10.17:8080', user='python', password='', cachedir='/tmp')
        self.tmpdir   = '/home/xnat/tmp/cnc_converter'
        self.datafile = '/home/xnat/cnc_converter/data/cnc_data.pickle'
        self.logfile = '/home/xnat/cnc_converter/log/cnc_converter.log'
        self.database = {'test'}
        self.server_url = 'http://192.168.10.17:8080'
        logging.basicConfig(filename=self.logfile, format='[ %(asctime)s ] %(message)s ', level=logging.DEBUG)
        self.load_database()

        
    def __exit__(self):
        self.save_database()
        
    def projects(self):
        interface = self.interface
        projects = interface.select.projects().get()
        return projects

    def subjects(self, projectname=""):
        interface = self.interface
        
        if (projectname == ""):
            subjects = interface.select.projects('*').subjects()
        else:
            subjects = interface.select.projects(projectname).subjects()
        return subjects
    
    def download_DICOM(subject):
        experiments = s.experiments()

        for e in experiments:
            dicoms = e.scans()

            for d in dicoms:
                str = d.get()
                xml = minidom.parseString(str)

                elm = xml.getElementsByTagName("xnat:MRScan")

            os.mkdir('/data/xnat/tmp/cnc_converter')
            dicoms.download('/data/xnat/tmp/cnc_converter/', type='ALL', extract=False)        

    def save_database(self):
        try:
            pickle.dump(self.database, open(self.datafile, "wb"))            
            logging.info('Database saved succesfully')
        except StandardError:
            logging.error("Could not open database file")

    def load_database(self):
        if os.path.isfile(self.datafile):
            try:
                self.database = pickle.load(open(self.datafile, "rb"));
            except StandardError:
                logging.error('Database could not be loaded')
                pass
        logging.info('Database loaded')
        
            
    def process(self):
        subjects = self.subjects();

        logging.info('Found %d subjects', subjects.__sizeof__())
        for s in subjects:
            self.download_DICOM(s)
            
            


        
    

c = CNC_Converter()
c.save_database()
c.process()
