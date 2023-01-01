import json


def user_search_response_template(status, content, username):
    if status:
        success_template = {
            "ok": status,
            "data": {
                "username": username,
                "lastHourUsage": content,
                "last6HourUsage": content,
                "last24HourUsage": content,
            }
        }

        success_template_json = json.dumps(success_template, indent=4)
        return success_template_json


def usage_info_response_template(status, content, page_size, page, total_pages):
    if status == 1:
        success_template = {
            "ok": True,
            "data": content,
            "pageSize": page_size,
            "page": page,
            "totalPages": total_pages,
        }

        success_template_json = json.dumps(success_template, indent=4)
        return success_template_json


def invalid_page_scenario():
    semi_success_template = {
        "ok": True,
        "data": [],

    }
    semi_success_template_json = json.dumps(semi_success_template, indent=4)
    return semi_success_template_json


def usage_info_response_template_failure(content):
    failure_template = {
        "ok": False,
        "error":
            {
                "message": content.get("error_msg")
            }
    }
    failure_template_json = json.dumps(failure_template, indent=4)
    return failure_template_json


def user_data_template():
    mp = {
        "username": "",
        "lastDayUsage": "",
        "last7DayUsage": "",
        "last30DayUsage": "",

    }

    return mp


def search_data_template():
    mp = {
        "time": "",
        "upload": "",
        "download": "",
    }
    return mp
