from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.base_entity import BaseEntity


class PushNotificationSubscriber(BaseEntity):
    """Represents a push notification subscriber over a site."""

    @property
    def custom_args(self):
        """Gets the custom arguments specified by the app.

        :rtype: str
        """
        return self.properties.get("CustomArgs", None)

    @property
    def service_token(self):
        """Specifies the delivery channel URI for push notifications. It must not be null. It must not be empty.

        :rtype: str
        """
        return self.properties.get("ServiceToken", None)

    @service_token.setter
    def service_token(self, value):
        """
        Specifies the delivery channel URI for push notifications. It must not be null. It must not be empty.

        :type value: str
        """
        self.set_property("ServiceToken", value)

    @property
    def user(self):
        """Gets the SharePoint user who created this subscriber."""
        from office365.sharepoint.principal.user import User
        return self.properties.get("User", User(self.context, ResourcePath("user", self.resource_path)))
