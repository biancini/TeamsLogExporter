from office365.directory.identities.userflows.language_page import UserFlowLanguagePage
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class UserFlowLanguageConfiguration(Entity):
    """Allows a user flow to support the use of multiple languages.

       For Azure Active Directory user flows, you can only leverage the built-in languages provided by Microsoft.
       User flows for Azure Active Directory support defining the language and strings shown to users
       as they go through the journeys you configure with your user flows."""

    @property
    def display_name(self):
        """
        The language name to display.

        :rtype: str or None
        """
        return self.properties.get("displayName", None)

    @property
    def default_pages(self):
        """Collection of pages with the default content to display in a user flow for a specified language.

        :rtype: EntityCollection
        """
        return self.get_property('defaultPages',
                                 EntityCollection(self.context, UserFlowLanguagePage,
                                                  ResourcePath("defaultPages", self.resource_path)))

    @property
    def overrides_pages(self):
        """Collection of pages with the default content to display in a user flow for a specified language.

        :rtype: EntityCollection
        """
        return self.get_property('overridesPages',
                                 EntityCollection(self.context, UserFlowLanguagePage,
                                                  ResourcePath("overridesPages", self.resource_path)))

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "defaultPages": self.default_pages,
                "overridesPages": self.overrides_pages
            }
            default_value = property_mapping.get(name, None)
        return super(UserFlowLanguageConfiguration, self).get_property(name, default_value)
