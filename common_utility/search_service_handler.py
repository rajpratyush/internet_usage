import datetime
import math

from common_utility import constant_method
from info_tools.models import InternetUsageData


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class SearchServiceHandler:

    @staticmethod
    def fetch_user_data(user_name):
        # response = {'status': False, 'msg': "Error occurred while fetching user data"}
        # try:
        check_usr_exit = InternetUsageData.objects.filter(username=user_name).exists()

        if not check_usr_exit:
            response = {'status': False, 'msg': "user not found"}
            return response

        latest_entry = InternetUsageData.objects.filter(username=user_name).order_by('-start_time')[0]

        last_entry_datetime = latest_entry.start_time

        last_user_entry = InternetUsageData.objects.filter(username=user_name,
                                                           start_time__date=last_entry_datetime.date()).order_by(
            '-start_time')

        content_template = constant_method.search_data_template()

        start_time_res = None
        upload_res = None
        download_res = None
        for value in last_user_entry:
            st = value.start_time
            up = value.upload
            download = value.download

            if start_time_res is None:
                start_time_res = datetime.timedelta(hours=int(st.hour), minutes=int(st.minute),
                                                    seconds=int(st.second))
            else:
                start_time_res += datetime.timedelta(hours=int(st.hour), minutes=int(st.minute),
                                                     seconds=int(st.second))
            if upload_res is None:
                upload_res = up
            else:
                upload_res += up

            if download_res is None:
                download_res = download
            else:
                download_res += download

        content_template.__setitem__('time', start_time_res.__str__())
        content_template.__setitem__('upload', convert_size(upload_res * 10 ** 3))
        content_template.__setitem__('download', convert_size(download_res * 10 ** 3))

        response = {'status': True, 'msg': "operation executed successfully", 'output': content_template}

        return response

        # except (Exception,) as err:
        #     print(err)
        #     return response
