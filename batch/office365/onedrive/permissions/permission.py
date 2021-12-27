from office365.directory.identities.identity_set import IdentitySet
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.drives.drive_recipient import DriveRecipient
from office365.onedrive.listitems.item_reference import ItemReference
from office365.onedrive.permissions.sharing_invitation import SharingInvitation
from office365.onedrive.permissions.sharing_link import SharingLink
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation_query import ServiceOperationQuery
from office365.runtime.paths.resource_path import ResourcePath


class Permission(Entity):
    """The Permission resource provides information about a sharing permission granted for a DriveItem resource."""

    def grant(self, recipients, roles):
        """
        Grant users access to a link represented by a permission.

        :param list[str] recipients: A collection of recipients who will receive access.
        :param list[str] roles: If the link is an "existing access" link, specifies roles to be granted to the users.
            Otherwise must match the role of the link.
        """
        payload = {
            "recipients": ClientValueCollection(DriveRecipient, [DriveRecipient.from_email(r) for r in recipients]),
            "roles": ClientValueCollection(str, roles)
        }
        return_type = EntityCollection(self.context, Permission, ResourcePath("permissions", self.resource_path))
        qry = ServiceOperationQuery(self, "grant", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def invitation(self):
        """For user type permissions, the details of the users & applications for this permission."""
        return self.properties.get('invitation', SharingInvitation())

    @property
    def granted_to(self):
        """For user type permissions, the details of the users & applications for this permission."""
        return self.properties.get('grantedTo', IdentitySet())

    @property
    def granted_to_identities(self):
        """For link type permissions, the details of the users to whom permission was granted. Read-only."""
        return self.properties.get('grantedToIdentities', ClientValueCollection(IdentitySet))

    @property
    def link(self):
        """Provides the link details of the current permission, if it is a link type permissions. Read-only."""
        return self.properties.get('link', SharingLink())

    @property
    def roles(self):
        """The type of permission, e.g. read. See below for the full list of roles. Read-only."""
        return self.properties.get('roles', ClientValueCollection(str))

    @roles.setter
    def roles(self, value):
        """
        Sets the type of permission

        :type value: list[str]
        """
        self.set_property("roles", ClientValueCollection(str, value))

    @property
    def share_id(self):
        """A unique token that can be used to access this shared item via the shares API. Read-only.

        :rtype: str
        """
        return self.properties.get('shareId', None)

    @property
    def has_password(self):
        """This indicates whether password is set for this permission, it's only showing in response.
        Optional and Read-only and for OneDrive Personal only.

        :rtype: bool
        """
        return self.properties.get('hasPassword', None)

    @property
    def inherited_from(self):
        """
        If this content type is inherited from another scope (like a site),
        provides a reference to the item where the content type is defined.
        """
        return self.properties.get("inheritedFrom", ItemReference())

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "inheritedFrom": self.inherited_from,
                "grantedTo": self.granted_to,
                "grantedToIdentities": self.granted_to_identities
            }
            default_value = property_mapping.get(name, None)
        return super(Permission, self).get_property(name, default_value)
