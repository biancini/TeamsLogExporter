from datetime import datetime

from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.base_entity import BaseEntity


class Subscription(BaseEntity):
    """A subscription for receiving notifications at a specified endpoint."""

    @property
    def notification_url(self):
        """
        Gets endpoint that will be called when an event occurs.

        :rtype: str
        """
        return self.properties.get("notificationUrl", None)

    @notification_url.setter
    def notification_url(self, value):
        """
        Sets endpoint that will be called when an event occurs.
        """
        self.set_property("notificationUrl", value)

    @property
    def expiration_datetime(self):
        """
        Gets endpoint that will be called when an event occurs.

        :rtype: str
        """
        return self.properties.get("expirationDateTime", None)

    @expiration_datetime.setter
    def expiration_datetime(self, value):
        """
        Sets endpoint that will be called when an event occurs.
        """
        if isinstance(value, datetime):
            self.set_property("expirationDateTime", value.isoformat())
        else:
            self.set_property("expirationDateTime", value)

    def set_property(self, name, value, persist_changes=True):
        # fallback: create a new resource path
        if self._resource_path is None:
            if name == "id":
                self._resource_path = ServiceOperationPath("getById",
                                                           [value], self._parent_collection.resource_path)
        return super(Subscription, self).set_property(name, value, persist_changes)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Webhooks.Subscription"
