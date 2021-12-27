from office365.runtime.queries.create_entity_query import CreateEntityQuery
from office365.runtime.queries.service_operation_query import ServiceOperationQuery
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.base_entity_collection import BaseEntityCollection
from office365.sharepoint.lists.list import List


class ListCollection(BaseEntityCollection):
    """Lists collection"""

    def __init__(self, context, resource_path=None):
        super(ListCollection, self).__init__(context, List, resource_path)

    def get_by_title(self, list_title):
        """Retrieve List client object by title

        :type list_title: str
        """
        return List(self.context,
                    ServiceOperationPath("GetByTitle", [list_title], self.resource_path))

    def get_by_id(self, list_id):
        """Retrieve List client object by id

        :type list_id: str
        """
        return List(self.context,
                    ServiceOperationPath("GetById", [list_id], self.resource_path))

    def ensure_events_list(self):
        events_list = List(self.context)
        self.add_child(events_list)
        qry = ServiceOperationQuery(self, "EnsureEventsList", None, None, None, events_list)
        self.context.add_query(qry)
        return events_list

    def ensure_site_assets_library(self):
        """Gets a list that is the default asset location for images or other files, which the users
        upload to their wiki pages."""
        target_list = List(self.context)
        self.add_child(target_list)
        qry = ServiceOperationQuery(self, "ensureSiteAssetsLibrary", None, None, None, target_list)
        self.context.add_query(qry)
        return target_list

    def ensure_site_pages_library(self):
        """Gets a list that is the default location for wiki pages."""
        target_list = List(self.context)
        self.add_child(target_list)
        qry = ServiceOperationQuery(self, "ensureSitePagesLibrary", None, None, None, target_list)
        self.context.add_query(qry)
        return target_list

    def add(self, list_creation_information):
        """Creates a List resource

        :type list_creation_information: office365.sharepoint.lists.list_creation_information.ListCreationInformation
        """
        target_list = List(self.context)
        self.add_child(target_list)
        qry = CreateEntityQuery(self, list_creation_information, target_list)
        self.context.add_query(qry)
        return target_list
