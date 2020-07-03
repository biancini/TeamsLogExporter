from office365.runtime.odata.odata_path_parser import ODataPathParser
from office365.runtime.resource_path import ResourcePath


class ResourcePathServiceOperation(ResourcePath):
    """ Resource path to address Service Operations which
    represents simple functions exposed by an OData service"""

    def __init__(self, method_name, method_parameters=None, parent=None):
        """
        :type method_parameters: list or dict or office365.runtime.clientValue.ClientValue
        :type method_name: str


        """
        super(ResourcePathServiceOperation, self).__init__(ODataPathParser.from_method(method_name, method_parameters),
                                                           parent)
