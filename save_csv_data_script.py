"""
File_Name = save_csv_script.py
Purpose: This script helps to migrate csv data to django model
How to run this script:

Open Django Project where you find manage.py

on the same python open terminal and write following commands'
python manage.py shell
exec(open(save_csv_data_script.py).read())

"""

from common_utility.csv_reader import save_csv_data_to_db

save_csv_data_to_db()
