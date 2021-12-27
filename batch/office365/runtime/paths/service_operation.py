from office365.runtime.client_path import ClientPath
from office365.runtime.odata.odata_path_builder import ODataPathBuilder


class ServiceOperationPath(ClientPath):
    """ Resource path to address Service Operations which
    represents simple functions exposed by an OData service"""

    def __init__(self, name, parameters=None, parent=None):
        """
        :type parameters: list or dict or office365.runtime.client_value.ClientValue or None
        :type name: str
        :type parent: office365.runtime.client_path.ClientPath
        """
        super(ServiceOperationPath, self).__init__(parent)
        self._name = name
        self._parameters = parameters

    @property
    def segments(self):
        return [self.delimiter, ODataPathBuilder.from_operation(self._name, self._parameters)]
