from office365.runtime.client_value import ClientValue


class SharingLinkAccessRequest(ClientValue):

    def __init__(self):
        super(SharingLinkAccessRequest, self).__init__()
        self.ensureAccess = None
        self.password = None
