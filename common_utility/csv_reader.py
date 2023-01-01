"""
File_Name = csv_reader.py
Purpose: This script helps to migrate csv data to django model

"""

import csv
from common_utility import constant
from info_tools.models import InternetUsageData


def save_csv_data_to_db():
    response = {'status': False, 'msg': "Error Occurred while saving data from csv to database"}
    with open(constant.CSV_FILE_LOCATION) as file:
        csvreader = csv.reader(file)

        delete_status = bool(InternetUsageData.objects.all().delete())

        if not delete_status:
            response['msg'] += " Failed to delete previous data from database"
            return response
        for index, row in enumerate(csvreader):
            if index == 0:
                continue
            else:
                print(index, row[0], row[1])
                InternetUsageData.objects.get_or_create(username=row[0],
                                                        mac_address=row[1],
                                                        start_time=row[2],
                                                        usage_time=row[3],
                                                        upload=row[4],
                                                        download=row[5])

    response = {'status': True, 'msg': "Latest data from csv saved in database"}
    return response
