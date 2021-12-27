from office365.sharepoint.base_entity import BaseEntity


class SiteProperties(BaseEntity):
    """Contains a property bag of information about a site."""

    def __init__(self, context):
        super(SiteProperties, self).__init__(context)

    def set_property(self, name, value, persist_changes=True):
        super(SiteProperties, self).set_property(name, value, persist_changes)
        # fallback: create a new resource path
        if name == "Url" and self._resource_path is None:
            pass
            # site_ctx = self.context.clone(value)
            # target_site = site_ctx.site
            # site_ctx.load(target_site)
            # site_ctx.execute_query()
            # self._resource_path = ResourcePathServiceOperation(
            #    "getById", [target_site.properties['Id']], self._parent_collection.resource_path)

    @property
    def url(self):
        """

        :rtype: str
        """
        return self.properties.get('Url', None)

    @property
    def compatibilityLevel(self):
        """
        Gets the compatibility level of the site.

        :rtype: str
        """
        return self.properties.get('CompatibilityLevel', None)

    @property
    def lock_state(self):
        """
        Gets or sets the lock state of the site.

        :rtype: str
        """
        return self.properties.get('LockState', None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteProperties"
