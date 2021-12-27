from office365.runtime.client_value import ClientValue


class UploadSession(ClientValue):
    """The UploadSession resource provides information about how to upload large files to OneDrive, OneDrive for
    Business, or SharePoint document libraries. """

    def __init__(self):
        super(UploadSession, self).__init__()
        self.expirationDateTime = None
        self.nextExpectedRanges = None
        self.uploadUrl = None
