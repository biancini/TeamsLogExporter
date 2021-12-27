from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation_query import ServiceOperationQuery
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.base_entity import BaseEntity
from office365.sharepoint.principal.user import User
from office365.sharepoint.tenant.management.users_results import GetExternalUsersResults, RemoveExternalUsersResults, \
    SPOUserSessionRevocationResult
from office365.sharepoint.tenant.administration.theme_properties import ThemeProperties


class Office365Tenant(BaseEntity):
    """Represents a SharePoint Online tenant."""

    @property
    def allow_editing(self):
        return self.properties.get("AllowEditing", None)

    def __init__(self, context):
        super(Office365Tenant, self).__init__(
            context,
            ResourcePath("Microsoft.Online.SharePoint.TenantManagement.Office365Tenant")
        )

    def add_tenant_cdn_origin(self, cdn_type, origin_url):
        """
        Configures a new origin to public or private CDN, on either Tenant level or on a single Site level.
        Effectively, a tenant admin points out to a document library, or a folder in the document library
        and requests that content in that library should be retrievable by using a CDN.

        You must have the SharePoint Admin role or Global Administrator role and be a site collection administrator
        to run the operation.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        :param str origin_url: Specifies a path to the doc library to be configured. It can be provided in two ways:
            relative path, or a mask.
        """
        payload = {
            "cdnType": cdn_type,
            "originUrl": origin_url,
        }
        qry = ServiceOperationQuery(self, "AddTenantCdnOrigin", None, payload)
        self.context.add_query(qry)
        return self

    def get_tenant_cdn_enabled(self, cdn_type):
        """
        Returns whether Public content delivery network (CDN) or Private CDN is enabled on the tenant level.

        You must have the SharePoint Admin role or Global Administrator role and be a site collection administrator
        to run the operation.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        """
        payload = {
            "cdnType": cdn_type,
        }
        return_type = ClientResult(self.context)
        qry = ServiceOperationQuery(self, "GetTenantCdnEnabled", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def set_tenant_cdn_enabled(self, cdn_type, is_enabled):
        """
        Enables or disables Public content delivery network (CDN) or Private CDN on the tenant level.

        You must have the SharePoint Admin role or Global Administrator role and be a site collection administrator
        to run the operation.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        :param bool is_enabled: Specifies if the CDN is enabled.
        """
        payload = {
            "cdnType": cdn_type,
            "isEnabled": is_enabled
        }
        qry = ServiceOperationQuery(self, "SetTenantCdnEnabled", None, payload)
        self.context.add_query(qry)
        return self

    def remove_tenant_cdn_origin(self, cdn_type, origin_url):
        """
        Removes a new origin from the Public or Private content delivery network (CDN).

        You must have the SharePoint Admin role or Global Administrator role and be a site collection administrator
        to run the operation.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        :param str origin_url: Specifies a path to the doc library to be configured. It can be provided in two ways:
            relative path, or a mask.
        """
        payload = {
            "cdnType": cdn_type,
            "originUrl": origin_url,
        }
        qry = ServiceOperationQuery(self, "RemoveTenantCdnOrigin", None, payload)
        self.context.add_query(qry)
        return self

    def get_tenant_cdn_policies(self, cdn_type):
        """
        Get the public or private Policies applied on your SharePoint Online Tenant.

        Requires Tenant administrator permissions.


        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        """
        payload = {
            "cdnType": cdn_type,
        }
        return_type = ClientResult(self.context, ClientValueCollection(str))
        qry = ServiceOperationQuery(self, "GetTenantCdnPolicies", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def set_tenant_cdn_policy(self, cdn_type, policy, policy_value):
        """
        Sets the content delivery network (CDN) policies at the tenant level.

        Requires Tenant administrator permissions.

        :param int cdn_type: Specifies the CDN type. The valid values are: public or private.
        :param int policy: The PolicyType specifies the type of policy to set.
               Valid values:
                  IncludeFileExtensions
                  ExcludeRestrictedSiteClassifications
                  ExcludeIfNoScriptDisabled
        :param str policy_value: A String representing the value of the policy type defined by the PolicyType parameter.
        """
        payload = {
            "cdnType": cdn_type,
            "policy": policy,
            "policyValue": policy_value
        }
        qry = ServiceOperationQuery(self, "SetTenantCdnPolicy", None, payload)
        self.context.add_query(qry)
        return self

    def revoke_all_user_sessions(self, user_or_username):
        """
        Provides IT administrators the ability to invalidate a particular users' O365 sessions across all their devices.

        :param str or User user_or_username: Specifies a user name
              (for example, user1@contoso.com) or User object
        """
        return_type = SPOUserSessionRevocationResult(self.context)
        if isinstance(user_or_username, User):
            def _user_loaded():
                next_qry = ServiceOperationQuery(self, "RevokeAllUserSessions", [user_or_username.login_name], None,
                                                 None, return_type)
                self.context.add_query(next_qry)

            user_or_username.ensure_property("LoginName", _user_loaded)
        else:
            qry = ServiceOperationQuery(self, "RevokeAllUserSessions", [user_or_username], None, None, return_type)
            self.context.add_query(qry)
        return return_type

    def get_external_users(self, position=0, page_size=50, _filter=None, sort_order=0):
        """
        Returns external users in the tenant.

        :param int position: Use to specify the zero-based index of the position in the sorted collection of the
                             first result to be returned.
        :param int page_size: Specifies the maximum number of users to be returned in the collection.
                              The value must be less than or equal to 50.
        :param str _filter: Limits the results to only those users whose first name, last name, or email address
                            begins with the text in the string using a case-insensitive comparison.
        :param int sort_order: Specifies the sort results in Ascending or Descending order on the User.Email property
                               should occur.
        """
        return_type = GetExternalUsersResults(self.context)
        payload = {
            "position": position,
            "pageSize": page_size,
            "filter": _filter,
            "sortOrder": sort_order
        }
        qry = ServiceOperationQuery(self, "GetExternalUsers", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def remove_external_users(self, unique_ids=None):
        """
        Removes a collection of external users from the tenancy's folder.

        :param list[str] unique_ids: Specifies an ID that can be used to identify an external user based on
                                     their Windows Live ID.
        """
        payload = {
            "uniqueIds": unique_ids,
        }
        return_type = RemoveExternalUsersResults(self.context)
        qry = ServiceOperationQuery(self, "RemoveExternalUsers", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_all_tenant_themes(self):
        """
        Get all themes from tenant
        """
        return_type = ClientObjectCollection(self.context, ThemeProperties)
        qry = ServiceOperationQuery(self, "GetAllTenantThemes", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def add_tenant_theme(self, name, theme_json):
        """
        Adds a new theme to a tenant.

        :param str name:
        :param str theme_json:
        """
        return_type = ClientResult(self.context)
        payload = {
            "name": name,
            "themeJson": theme_json,
        }
        qry = ServiceOperationQuery(self, "AddTenantTheme", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def delete_tenant_theme(self, name):
        """
        Removes a theme from tenant

        :type name: str
        """
        payload = {
            "name": name,
        }
        qry = ServiceOperationQuery(self, "DeleteTenantTheme", None, payload)
        self.context.add_query(qry)
        return self

    def queue_import_profile_properties(self, id_type, source_data_id_property, property_map, source_uri):
        """Bulk import custom user profile properties

        :param int id_type: The type of id to use when looking up the user profile.
        :param str source_data_id_property: The name of the ID property in the source data.
        :param dict property_map: A map from the source property name to the user profile service property name.
        :param str source_uri: The URI of the source data file to import.
        """
        return_type = ClientResult(self.context)
        payload = {
            "idType": id_type,
            "sourceDataIdProperty": source_data_id_property,
            "propertyMap": property_map,
            "sourceUri": source_uri
        }
        qry = ServiceOperationQuery(self, "QueueImportProfileProperties", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type
