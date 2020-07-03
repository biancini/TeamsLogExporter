from office365.runtime.clientValue import ClientValue


class PasswordProfile(ClientValue):
    """Contains the password profile associated with a user. The passwordProfile property of the user entity is a
    passwordProfile object. """
    def __init__(self, password):
        super(PasswordProfile, self).__init__()
        self.password = password
        self.forceChangePasswordNextSignIn = True
