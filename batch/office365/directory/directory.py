from office365.directory.directory_object_collection import DirectoryObjectCollection
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class Directory(Entity):
    """Represents a deleted item in the directory. When an item is deleted, it is added to the deleted items
    "container". Deleted items will remain available to restore for up to 30 days. After 30 days, the items are
    permanently deleted. """

    def deleted_items(self, entity_type=None):
        """Recently deleted items. Read-only. Nullable."""
        if entity_type:
            return DirectoryObjectCollection(self.context,
                                             ResourcePath(entity_type,
                                                          ResourcePath("deletedItems", self.resource_path)))
        else:
            return self.properties.get('deletedItems',
                                       DirectoryObjectCollection(self.context,
                                                                 ResourcePath("deletedItems", self.resource_path)))

    @property
    def deleted_groups(self):
        """Recently deleted groups"""
        return self.deleted_items("microsoft.graph.group")

    @property
    def deleted_users(self):
        """Recently deleted users"""
        return self.deleted_items("microsoft.graph.user")

    @property
    def deleted_applications(self):
        """Recently deleted applications"""
        return self.deleted_items("microsoft.graph.application")
