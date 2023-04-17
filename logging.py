import csv
import os.path
import asyncio

class ServerLogging(object):
    def __init__(self):
        self.ClientIP = None
        self.AccessTime = None
        self.RequestedFileName = None
        self.ResponseType = None
        self.HeaderList = ["Access Time", "Client IP", "HTTP Response Status", "Requested File Name", ]


    def CheckFileExtension(self):
        Path = "log.csv"
        existance = os.path.exists(Path)

        # File doesn't exist 
        if existance == False:
            self.CSVFileCreation()

        else:
            # compare column headers to check file vaildity
            # https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
            with open("log.csv", "r", newline="") as file:
                reader = csv.DictReader(file, delimiter=',', quotechar='"')
                ColumnList = []

                for row in reader:
                    ColumnList.append(row)
                    # We just want the column headers
                    break

            if ColumnList != self.HeaderList:
                self.CSVFileCreation()


    def CSVFileCreation(self):
        with open("log.csv", "w", newline="") as file:
            Log = csv.DictWriter(file,  delimiter=",",  fieldnames=self.HeaderList)
            Log.writeheader()


    def FormDate(self):
        dict = {
                "Access Time": self.AccessTime, 
                "Client IP": self.ClientIP
               }