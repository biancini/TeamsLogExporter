from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation_query import ServiceOperationQuery
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.administration.org_assets import OrgAssets
from office365.sharepoint.base_entity import BaseEntity
from office365.sharepoint.files.file import File
from office365.sharepoint.publishing.communication_site import CommunicationSite
from office365.sharepoint.publishing.file_picker_options import FilePickerOptions
from office365.sharepoint.publishing.primary_city_time import PrimaryCityTime
from office365.sharepoint.publishing.site_page_collection import SitePageCollection


class SitePageService(BaseEntity):

    def __init__(self, context, resource_path=None):
        """Represents a set of APIs to use for managing site pages."""
        if resource_path is None:
            resource_path = ResourcePath("SP.Publishing.SitePageService")
        super(SitePageService, self).__init__(context, resource_path)

    @property
    def pages(self):
        return self.properties.get("pages",
                                   SitePageCollection(self.context, ResourcePath("pages", self.resource_path)))

    @property
    def communication_site(self):
        return self.properties.get("CommunicationSite",
                                   CommunicationSite(self.context,
                                                     ResourcePath("CommunicationSite", self.resource_path)))

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageService"

    @staticmethod
    def can_create_promoted_page(context):
        """
        Checks if the current user has permission to create a site page on the site pages document library.
        MUST return true if the user has permission to create a site page, otherwise MUST return false.

        :param office365.sharepoint.client_context.ClientContext context: SharePoint context
        """
        return_type = ClientResult(context)
        svc = SitePageService(context)
        qry = ServiceOperationQuery(svc, "CanCreatePromotedPage", None, None, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_time_zone(context, city_name):
        """
        Gets time zone data for specified city.

        :param office365.sharepoint.client_context.ClientContext context:
        :param str city_name: The name of the city.
        :return: PrimaryCityTime
        """
        return_type = PrimaryCityTime(context)
        svc = SitePageService(context)
        params = {"cityName": city_name}
        qry = ServiceOperationQuery(svc, "GetTimeZone", params, None, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def compute_file_name(context, title):
        """

        :param office365.sharepoint.client_context.ClientContext context: Client context
        :param str title: The title of the page.
        """
        return_type = ClientResult(context)
        svc = SitePageService(context)
        params = {"title": title}
        qry = ServiceOperationQuery(svc, "ComputeFileName", params, None, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_available_full_page_applications():
        pass

    @staticmethod
    def get_current_user_memberships():
        pass

    @staticmethod
    def is_file_picker_external_image_search_enabled():
        pass

    @staticmethod
    def org_assets(context):
        """

        :param office365.sharepoint.client_context.ClientContext context: Client context
        """
        result = ClientResult(context, OrgAssets())
        svc = SitePageService(context)
        qry = ServiceOperationQuery(svc, "OrgAssets", None, None, None, result)
        qry.static = True
        context.add_query(qry)
        return result

    @staticmethod
    def file_picker_tab_options(context):
        """

        :param office365.sharepoint.client_context.ClientContext context: Client context
        """
        result = ClientResult(context, FilePickerOptions())
        svc = SitePageService(context)
        qry = ServiceOperationQuery(svc, "FilePickerTabOptions", None, None, None, result)
        qry.static = True
        context.add_query(qry)
        return result

    def add_image(self, page_name, image_file_name, image_stream):
        """
        Adds an image to the site assets library of the current web.
        Returns a File object ([MS-CSOMSPT] section 3.2.5.64) that represents the image.

        :param str image_stream: The image stream.
        :param str image_file_name: Indicates the file name of the image to be added.
        :param str page_name: Indicates the name of that site page that the image is to be used in.
        :return: File
        """
        return_type = File(self.context)
        params = {"pageName": page_name, "imageFileName": image_file_name, "imageStream": image_stream}
        qry = ServiceOperationQuery(self, "AddImage", params, None, None, return_type)
        qry.static = True
        self.context.add_query(qry)
        return return_type

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "CommunicationSite": self.communication_site,
            }
            default_value = property_mapping.get(name, None)
        return super(SitePageService, self).get_property(name, default_value)
