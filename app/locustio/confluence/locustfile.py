from extension.confluence.extension_locust import get_template_list, find_page_by_event_id_not_found, \
    find_page_by_event_id_found
from locust import HttpUser, task, between
from locustio.common_utils import LocustConfig, MyBaseTaskSet
from locustio.confluence.http_actions import login_and_view_dashboard, view_dashboard, view_blog, \
    search_cql_and_view_results, open_editor_and_create_blog, create_and_edit_page, comment_page, view_attachments, \
    upload_attachments, like_page, view_page
from util.conf import CONFLUENCE_SETTINGS

config = LocustConfig(config_yml=CONFLUENCE_SETTINGS)


class ConfluenceBehavior(MyBaseTaskSet):

    def on_start(self):
        self.client.verify = config.secure
        login_and_view_dashboard(self)

    @task(config.percentage('view_page'))
    def view_page_action(self):
        view_page(self)

    @task(config.percentage('view_dashboard'))
    def view_dashboard_action(self):
        view_dashboard(self)

    @task(config.percentage('view_blog'))
    def view_blog_action(self):
        view_blog(self)

    @task(config.percentage('search_cql'))
    def search_cql_action(self):
        search_cql_and_view_results(self)

    @task(config.percentage('create_blog'))
    def create_blog_action(self):
        open_editor_and_create_blog(self)

    @task(config.percentage('create_and_edit_page'))
    def create_and_edit_page_action(self):
        create_and_edit_page(self)

    @task(config.percentage('comment_page'))
    def comment_page_action(self):
        comment_page(self)

    @task(config.percentage('view_attachment'))
    def view_attachments_action(self):
        view_attachments(self)

    @task(config.percentage('upload_attachment'))
    def upload_attachments_action(self):
        upload_attachments(self)

    @task(config.percentage('like_page'))
    def like_page_action(self):
        like_page(self)

    # @task(config.percentage('standalone_extension'))
    # def custom_action(self):
    #     app_specific_action(self)

    @task(config.percentage('standalone_extension_get_template_list'))
    def get_template_list_action(self):
        get_template_list(self)

    @task(config.percentage('standalone_extension_find_page_by_event_id_found'))
    def find_page_by_event_id_action_found(self):
        find_page_by_event_id_found(self)

    @task(config.percentage('standalone_extension_find_page_by_event_id_not_found'))
    def find_page_by_event_id_action_not_found(self):
        find_page_by_event_id_not_found(self)


class ConfluenceUser(HttpUser):
    host = CONFLUENCE_SETTINGS.server_url
    tasks = [ConfluenceBehavior]
    wait_time = between(0, 0)
