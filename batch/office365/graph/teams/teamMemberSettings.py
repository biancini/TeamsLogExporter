from office365.runtime.clientValue import ClientValue


class TeamMemberSettings(ClientValue):
    """Settings to configure whether members can perform certain actions, for example, create channels and add bots,
    in the team. """

    def __init__(self):
        super().__init__()
        self.allowCreateUpdateChannels = True
        self.allowDeleteChannels = True
        self.allowAddRemoveApps = True
        self.allowCreateUpdateRemoveTabs = True
        self.allowCreateUpdateRemoveConnectors = True






