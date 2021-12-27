from office365.base_item import BaseItem
from office365.entity_collection import EntityCollection
from office365.onedrive.contenttypes.content_type_info import ContentTypeInfo
from office365.onedrive.listitems.field_value_set import FieldValueSet
from office365.onedrive.analytics.item_analytics import ItemAnalytics
from office365.onedrive.versions.list_item_version import ListItemVersion
from office365.runtime.paths.resource_path import ResourcePath


class ListItem(BaseItem):
    """Represents an item in a SharePoint list. Column values in the list are available through the fieldValueSet
    dictionary. """

    @property
    def fields(self):
        """The values of the columns set on this list item."""
        return self.properties.get('fields',
                                   FieldValueSet(self.context, ResourcePath("fields", self.resource_path)))

    @property
    def versions(self):
        """The list of previous versions of the list item."""
        return self.properties.get('versions',
                                   EntityCollection(self.context, ListItemVersion,
                                                    ResourcePath("versions", self.resource_path)))

    @property
    def drive_item(self):
        """For document libraries, the driveItem relationship exposes the listItem as a driveItem."""
        from office365.onedrive.driveitems.driveItem import DriveItem
        return self.properties.get('driveItem', DriveItem(self.context, ResourcePath("driveItem", self.resource_path)))

    @property
    def content_type(self):
        """The content type of this list item"""
        return self.properties.get("contentType", ContentTypeInfo())

    @property
    def analytics(self):
        """Analytics about the view activities that took place on this item."""
        return self.properties.get('analytics',
                                   ItemAnalytics(self.context, ResourcePath("analytics", self.resource_path)))

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "contentType": self.content_type,
                "driveItem": self.drive_item
            }
            default_value = property_mapping.get(name, None)
        return super(ListItem, self).get_property(name, default_value)

