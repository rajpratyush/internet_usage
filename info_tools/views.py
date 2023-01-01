from django.http import HttpResponse

from common_utility import constant_method
from common_utility.search_service_handler import SearchServiceHandler
from common_utility.usage_service_handler import UsageServiceHandler


def analytics(request):
    date = request.GET.get('date') if request.GET.get('date') else ""
    limit = int(request.GET.get('limit')) if request.GET.get('limit') else ""
    page = int(request.GET.get('page')) if request.GET.get('page') else ""

    if limit == "" or page == "":
        content = {'error_msg': "blank parameter passed"}
        template = constant_method.usage_info_response_template_failure(content)
        return HttpResponse(template, content_type='application/json')


    else:
        object_usage = UsageServiceHandler()
        get_data = object_usage.serialize_parameter(date, limit, page)

        if get_data['status'] == -1:
            content = {'error_msg': get_data['msg']}
            template = constant_method.usage_info_response_template_failure(content)
            return HttpResponse(template, content_type='application/json')
        elif get_data['status'] == 0:
            template = constant_method.invalid_page_scenario()
            return HttpResponse(template, content_type='application/json')
        elif get_data['status'] == 1:

            template = constant_method.usage_info_response_template(get_data['status'], get_data['output'],
                                                                    get_data['page_size'], get_data['page'],
                                                                    get_data['total_pages'])
            return HttpResponse(template, content_type='application/json')

    return HttpResponse({"status": False, "message": "unable to process request"}, content_type='application/json')


def search(request):
    username = str(request.GET.get('username')) if request.GET.get('username') else ""

    if username == "":
        content = {'error_msg': "blank parameter passed"}
        template = constant_method.usage_info_response_template_failure(content)
        return HttpResponse(template, content_type='application/json')

    else:
        object_search = SearchServiceHandler()

        get_user_data_res = object_search.fetch_user_data(username)

        if not get_user_data_res['status']:
            content = {'error_msg': get_user_data_res['msg']}
            template = constant_method.usage_info_response_template_failure(content)
            return HttpResponse(template, content_type='application/json')
        else:

            template = constant_method.user_search_response_template(get_user_data_res['status'],
                                                                     get_user_data_res['output'], username)
            print(template)
            return HttpResponse(template, content_type='application/json')
