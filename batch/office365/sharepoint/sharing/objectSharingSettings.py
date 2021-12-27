from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.base_entity import BaseEntity
from office365.sharepoint.sharing.object_sharing_information import ObjectSharingInformation
from office365.sharepoint.sharing.sharePointSharingSettings import SharePointSharingSettings
from office365.sharepoint.sharing.sharingPermissionInformation import SharingPermissionInformation


class ObjectSharingSettings(BaseEntity):

    @property
    def web_url(self):
        """

        :return: str
        """
        return self.properties.get("WebUrl", None)

    @property
    def access_request_mode(self):
        """

        :return: bool
        """
        return self.properties.get("AccessRequestMode", None)

    @property
    def can_send_email(self):
        """

        :return: bool
        """
        return self.properties.get("CanSendEmail", None)

    @property
    def is_user_site_admin(self):
        """

        :return: bool
        """
        return self.properties.get("IsUserSiteAdmin", None)

    @property
    def object_sharing_information(self):
        return self.properties.get("ObjectSharingInformation",
                                   ObjectSharingInformation(self.context,
                                                            ResourcePath("ObjectSharingInformation",
                                                                         self.resource_path)))

    @property
    def sharepoint_settings(self):
        return self.properties.get("SharePointSettings",
                                   SharePointSharingSettings(self.context,
                                                             ResourcePath("SharePointSettings", self.resource_path)))

    @property
    def sharing_permissions(self):
        return self.properties.get("SharingPermissions",
                                   SharingPermissionInformation(self.context,
                                                                ResourcePath("SharingPermissions", self.resource_path)))
