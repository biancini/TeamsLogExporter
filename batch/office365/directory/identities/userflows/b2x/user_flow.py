from office365.directory.identities.userflows.user_flow import IdentityUserFlow
from office365.directory.identities.userflows.language_configuration import UserFlowLanguageConfiguration
from office365.directory.identities.userflows.user_attribute_assignment import \
    IdentityUserFlowAttributeAssignmentCollection
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class B2XIdentityUserFlow(IdentityUserFlow):
    """
    Represents a self-service sign up user flow within an Azure Active Directory tenant.

    User flows are used to enable a self-service sign up experience for guest users on an application.
    User flows define the experience the end user sees while signing up, including which identity providers they can
    use to authenticate, along with which attributes are collected as part of the sign up process.
    """

    @property
    def languages(self):
        """The languages supported for customization within the user flow. Language customization is enabled by default
        in self-service sign-up user flow. You cannot create custom languages in self-service sign-up user flows.

        :rtype: EntityCollection
        """
        return self.get_property('languages',
                                 EntityCollection(self.context, UserFlowLanguageConfiguration,
                                                  ResourcePath("languages", self.resource_path)))

    @property
    def user_attribute_assignments(self):
        """The user attribute assignments included in the user flow.

        :rtype: IdentityUserFlowAttributeAssignmentCollection
        """
        return self.get_property('userAttributeAssignments',
                                 IdentityUserFlowAttributeAssignmentCollection(self.context,
                                                                               ResourcePath("userAttributeAssignments",
                                                                                            self.resource_path)))

    @property
    def user_flow_type(self):
        """
        The type of user flow. For self-service sign-up user flows,
        the value can only be signUpOrSignIn and cannot be modified after creation.

        :rtype: str or None
        """
        return self.properties.get('userFlowType', None)

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "userAttributeAssignments": self.user_attribute_assignments
            }
            default_value = property_mapping.get(name, None)
        return super(B2XIdentityUserFlow, self).get_property(name, default_value)
