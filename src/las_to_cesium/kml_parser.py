import numpy as np
import pandas as pd
import datetime
import xml.etree.ElementTree as ET


class KmlParser:

    def __init__(self, filename):
        self.filename = filename
        self.takeoff_datetime = None
        self.track = None

        self.parse(filename)

    def parse(self, file):

        tree = ET.parse(file)
        root = tree.getroot()

        takeoff_time_text = root.find('Folder')[-1].find('Metadata').find('FsInfo').attrib['time_of_first_point']
        self.takeoff_datetime = datetime.datetime.strptime(takeoff_time_text[:18], "%Y-%m-%dT%H:%M:%S")

        time_sec = np.array(
            root.find('Folder')[-1]
                .find('Metadata')
                .find('FsInfo')
                .find('SecondsFromTimeOfFirstPoint')
                .text.split(),
            dtype=int)

        time = [ self.takeoff_datetime + datetime.timedelta(seconds=int(t)) for t in time_sec ]

        track = np.array(
            [line.split(',') for line in root.find('Folder')[-1]
                .find('LineString')
                .find('coordinates')
                .text.split()],
            dtype=float)

        self.track = pd.DataFrame(zip(time, *track.T), columns=['time', 'longitude', 'latitude', 'altitude'] )


