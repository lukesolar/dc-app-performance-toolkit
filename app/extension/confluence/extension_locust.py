import random

from locustio.common_utils import init_logger, confluence_measure, run_as_specific_user  # noqa F401
from locustio.confluence.requests_params import confluence_datasets

logger = init_logger(app_type='confluence')
confluence_dataset = confluence_datasets()


@confluence_measure("locust_app_specific_get_template_list_action")
def get_template_list(locust):
    locust.get('/rest/meetical-api/1.0/template/list/TESTSPACE1', headers={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    })  # call app-specific GET endpoint


@confluence_measure("locust_app_specific_find_page_by_event_id_NOT_FOUND_action")
def find_page_by_event_id_not_found(locust):
    # try to find a page for event id event_id_invalid_{randomNr}
    event_id = "event_id_not_existing_" + str(random.randint(1, 5))
    with locust.get('/rest/api/content/search?cql=content.property[meetical].event.id%20IN%20("' + event_id + '")',
                    headers={
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate",
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest"
                    }, catch_response=True) as response:
        if response.status_code == 404:
            response.success()


@confluence_measure("locust_app_specific_find_page_by_event_id_FOUND_action")
def find_page_by_event_id_found(locust):
    # find page via event id for some random pages
    page = confluence_dataset["custom_pages"][random.randint(1, 5)]
    page_id = page[0]
    locust.get(
        '/rest/api/content/search?cql=content.property[meetical].event.id%20IN%20("event_id_for_page_' + page_id + '")',
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        })  # call app-specific GET endpoint
