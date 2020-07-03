from office365.graph.base_item import BaseItem
from office365.graph.onedrive.fieldValueSet import FieldValueSet
from office365.runtime.resource_path import ResourcePath


class ListItem(BaseItem):
    """Represents an item in a SharePoint list. Column values in the list are available through the fieldValueSet
    dictionary. """

    @property
    def fields(self):
        """The values of the columns set on this list item."""
        if self.is_property_available('fields'):
            return self.properties['fields']
        else:
            return FieldValueSet(self.context, ResourcePath("fields", self.resource_path))

    @property
    def driveItem(self):
        """For document libraries, the driveItem relationship exposes the listItem as a driveItem."""
        if self.is_property_available('driveItem'):
            return self.properties['driveItem']
        else:
            from office365.graph.onedrive.driveItem import DriveItem
            return DriveItem(self.context, ResourcePath("driveItem", self.resource_path))
