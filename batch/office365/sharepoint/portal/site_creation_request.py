from office365.runtime.client_value import ClientValue


class SPSiteCreationRequest(ClientValue):

    def __init__(self, title, url, owner=None):
        super(SPSiteCreationRequest, self).__init__()
        self.Title = title
        self.Url = url
        self.WebTemplate = "SITEPAGEPUBLISHING#0"
        self.Owner = owner
        self.Lcid = 1033
        self.ShareByEmailEnabled = False
        self.Classification = ""
        self.Description = ""
        self.SiteDesignId = "00000000-0000-0000-0000-000000000000"
        self.HubSiteId = "00000000-0000-0000-0000-000000000000"
        self.WebTemplateExtensionId = "00000000-0000-0000-0000-000000000000"

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.SPSiteCreationRequest"
