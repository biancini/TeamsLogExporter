from office365.entity_collection import EntityCollection
from office365.onenote.entity_hierarchy_model import OnenoteEntityHierarchyModel
from office365.onenote.sections.section import OnenoteSection
from office365.runtime.paths.resource_path import ResourcePath


class Notebook(OnenoteEntityHierarchyModel):
    """A OneNote notebook."""

    @property
    def sections(self):
        """Retrieve a list of onenoteSection objects from the specified notebook.

        :rtype: EntityCollection
        """
        return self.get_property('sections', EntityCollection(self.context, OnenoteSection,
                                                              ResourcePath("sections", self.resource_path)))

    @property
    def section_groups(self):
        """Retrieve a list of onenoteSection objects from the specified notebook.

        :rtype: EntityCollection
        """
        from office365.onenote.sectiongroups.section_group import SectionGroup
        return self.get_property('sectionGroups',
                                 EntityCollection(self.context, SectionGroup,
                                                  ResourcePath("sectionGroups", self.resource_path)))

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "sectionGroups": self.section_groups
            }
            default_value = property_mapping.get(name, None)
        return super(Notebook, self).get_property(name, default_value)
