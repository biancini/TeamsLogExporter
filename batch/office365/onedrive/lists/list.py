from office365.base_item import BaseItem
from office365.directory.subscriptions.subscription import Subscription
from office365.entity_collection import EntityCollection
from office365.onedrive.columns.column_definition import ColumnDefinition
from office365.onedrive.contenttypes.content_type import ContentType
from office365.onedrive.listitems.list_item import ListItem
from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath


class ListInfo(ClientValue):

    def __init__(self, template=None, content_types_enabled=False, hidden=False):
        super(ListInfo, self).__init__()
        self.template = template
        self.contentTypesEnabled = content_types_enabled
        self.hidden = hidden


class List(BaseItem):
    """The list resource represents a list in a site. This resource contains the top level properties of the list,
    including template and field definitions. """

    @property
    def list(self):
        """Provides additional details about the list."""
        return self.properties.get('list', ListInfo())

    @property
    def sharepoint_ids(self):
        """Returns identifiers useful for SharePoint REST compatibility."""
        return self.properties.get('sharepointIds', None)

    @property
    def drive(self):
        """Only present on document libraries. Allows access to the list as a drive resource with driveItems."""
        from office365.onedrive.drives.drive import Drive
        return self.get_property('drive',
                                 Drive(self.context, ResourcePath("drive", self.resource_path)))

    @property
    def columns(self):
        """The collection of columns under this site."""
        return self.get_property('columns',
                                 EntityCollection(self.context, ColumnDefinition,
                                                  ResourcePath("columns", self.resource_path)))

    @property
    def content_types(self):
        """The collection of content types under this site."""
        return self.get_property('contentTypes',
                                 EntityCollection(self.context, ContentType,
                                                  ResourcePath("contentTypes", self.resource_path)))

    @property
    def items(self):
        """All items contained in the list."""
        return self.get_property('items',
                                 EntityCollection(self.context, ListItem, ResourcePath("items", self.resource_path)))

    @property
    def subscriptions(self):
        """The set of subscriptions on the list."""
        return self.get_property('subscriptions',
                                 EntityCollection(self.context, Subscription,
                                                  ResourcePath("subscriptions", self.resource_path)))
