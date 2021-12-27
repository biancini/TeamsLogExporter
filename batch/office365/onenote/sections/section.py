from office365.entity_collection import EntityCollection
from office365.onenote.entity_hierarchy_model import OnenoteEntityHierarchyModel
from office365.onenote.operations.onenote_operation import OnenoteOperation
from office365.onenote.pages.page_links import PageLinks
from office365.runtime.queries.service_operation_query import ServiceOperationQuery
from office365.runtime.paths.resource_path import ResourcePath


class OnenoteSection(OnenoteEntityHierarchyModel):
    """A section in a OneNote notebook. Sections can contain pages."""

    def copy_to_section_group(self, group_id, _id, rename_as=None, site_collection_id=None, site_id=None):
        """For Copy operations, you follow an asynchronous calling pattern: First call the Copy action,
        and then poll the operation endpoint for the result.

        :param str group_id: The id of the group to copy to. Use only when copying to a Microsoft 365 group.
        :param str _id: Required. The id of the destination section group.
        :param str rename_as: The name of the copy. Defaults to the name of the existing item.
        :param str site_collection_id:
        :param str site_id:
        """
        return_type = OnenoteOperation(self.context)
        payload = {
            "groupId": group_id,
            "id": _id,
            "renameAs": rename_as,
            "siteCollectionId": site_collection_id,
            "siteId": site_id
        }
        qry = ServiceOperationQuery(self, "copyToSectionGroup", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def is_default(self):
        """Indicates whether this is the user's default section. Read-only."""
        return self.properties.get("isDefault", None)

    @property
    def links(self):
        """Links for opening the section. The oneNoteClientURL link opens the section in the OneNote native client
        if it's installed. The oneNoteWebURL link opens the section in OneNote on the web.

        """
        return self.properties.get("links", PageLinks())

    @property
    def pages(self):
        """
        The collection of pages in the section. Read-only. Nullable.

        :rtype: EntityCollection
        """
        from office365.onenote.pages.page import OnenotePage
        return self.get_property('pages',
                                 EntityCollection(self.context, OnenotePage, ResourcePath("pages", self.resource_path)))

    @property
    def parent_notebook(self):
        """The notebook that contains the page. Read-only.

        :rtype: Notebook
        """
        from office365.onenote.notebooks.notebook import Notebook
        return self.get_property('parentNotebook',
                                 Notebook(self.context, ResourcePath("parentNotebook", self.resource_path)))

    @property
    def parent_section_group(self):
        """The section group that contains the section. Read-only.

        :rtype: SectionGroup
        """
        from office365.onenote.sectiongroups.section_group import SectionGroup
        return self.get_property('parentSectionGroup',
                                 SectionGroup(self.context, ResourcePath("parentSectionGroup", self.resource_path)))

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "parentNotebook": self.parent_notebook,
                "parentSectionGroup": self.parent_section_group
            }
            default_value = property_mapping.get(name, None)
        return super(OnenoteSection, self).get_property(name, default_value)
