import datetime
from datetime import timedelta

from common_utility import constant_method
from info_tools.models import InternetUsageData


class UsageServiceHandler:

    @staticmethod
    def get_rows_by_slice(data, limit):
        paginated_data = []
        for start in range(0, len(data), limit):
            paginated_data.append(data[start:start + limit])
        return paginated_data

    def serialize_parameter(self, passed_date, limit, page):
        response = {'status': -1, 'msg': "Failed to analyse passed parameter"}
        try:
            date = int(passed_date[:2])
            month = int(passed_date[2:4])
            year = int(passed_date[4:])

            pass_db_date = None
            try:
                pass_db_date = datetime.datetime(year, month, date, 0, 0, 0, tzinfo=datetime.timezone.utc)
                correct_date = True
            except ValueError:
                correct_date = False

            if not correct_date:
                response = {'status': -1, 'msg': "invalid date"}
                return response

            # Fetch Data for specified date
            user_data_specific_date = list(
                InternetUsageData.objects.filter(start_time__date=pass_db_date).values_list('username', 'start_time',
                                                                                            'usage_time'))

            # Fetch Username list for specified date
            user_name = set()
            for values in user_data_specific_date:
                user_name.add(values[0])

            # Past data for specified user name
            usage_lst = user_data_specific_date.copy()
            for user_name_val in user_name:
                tmp_lst = list(InternetUsageData.objects.filter(
                    start_time__date__lt=pass_db_date,
                    username=user_name_val).order_by('-start_time').values_list('username', 'start_time',
                                                                                'usage_time'))
                usage_lst += tmp_lst

            content_lst = []
            for user in user_name:
                per_user_data_template = constant_method.user_data_template()
                per_user_data_template.__setitem__("username", user)
                time_count = None
                for value in user_data_specific_date:

                    if value[0] == user:
                        if time_count is None:
                            time_count = datetime.timedelta(hours=int(value[2].hour), minutes=int(value[2].minute),
                                                            seconds=int(value[2].second))


                        else:
                            time_count += datetime.timedelta(hours=int(value[2].hour), minutes=int(value[2].minute),
                                                             seconds=int(value[2].second))

                        per_user_data_template.__setitem__("lastDayUsage", time_count.__str__())

                content_lst.append(per_user_data_template)

            for item in content_lst:
                user_name = item.get('username')
                last_7_day = pass_db_date - timedelta(days=7)
                last_30_day = pass_db_date - timedelta(days=30)
                time_count_7 = None
                time_count_30 = None

                for value in usage_lst:

                    if value[0] == user_name and value[1] >= last_7_day:

                        if time_count_7 is None:

                            time_count_7 = datetime.timedelta(hours=int(value[2].hour), minutes=int(value[2].minute),
                                                              seconds=int(value[2].second))
                        else:
                            time_count_7 += datetime.timedelta(hours=int(value[2].hour), minutes=int(value[2].minute),
                                                               seconds=int(value[2].second))

                        item.__setitem__('last7DayUsage', time_count_7.__str__())

                    if value[0] == user_name and value[1] >= last_30_day:

                        if time_count_30 is None:
                            time_count_30 = datetime.timedelta(hours=int(value[2].hour), minutes=int(value[2].minute),
                                                               seconds=int(value[2].second))
                        else:
                            time_count_30 += datetime.timedelta(hours=int(value[2].hour), minutes=int(value[2].minute),
                                                                seconds=int(value[2].second))

                        item.__setitem__('last30DayUsage', time_count_30.__str__())

            paginated_usage_lst = self.get_rows_by_slice(content_lst, limit)
            n = len(content_lst)

            if page > n or page == 0:
                response = {'status': 0, 'msg': "Invalid Page Number"}
                return response
            else:
                response = {'status': 1, 'msg': "Invalid Page Number", 'output': paginated_usage_lst[page - 1],
                            'page_size': limit,
                            'page': page,
                            'total_pages': n,

                            }
                return response

        except (Exception,) as err:
            print(err)
            return response
