from office365.runtime.client_value import ClientValue
from office365.sharepoint.permissions.base_permissions import BasePermissions


class RoleDefinitionCreationInformation(ClientValue):

    def __init__(self):
        """Contains properties that are used as parameters to initialize a role definition."""
        super(RoleDefinitionCreationInformation, self).__init__()
        self.Name = None
        self.Description = None
        self.BasePermissions = BasePermissions()
