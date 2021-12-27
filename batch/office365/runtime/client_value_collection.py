from office365.runtime.client_value import ClientValue
from office365.runtime.odata.v3.json_light_format import JsonLightFormat


class ClientValueCollection(ClientValue):

    def __init__(self, item_type, initial_values=None):
        """
        :type item_type: any
        :type initial_values: [] or None
        """
        super(ClientValueCollection, self).__init__()
        if initial_values is None:
            initial_values = []
        self._data = initial_values
        self._item_type = item_type

    def add(self, value):
        self._data.append(value)

    def __getitem__(self, index):
        """

        :type index: int
        :rtype: ClientValue
        """
        return self._data[index]

    def __iter__(self):
        for item in self._data:
            yield item

    def __len__(self):
        return len(self._data)

    def to_json(self, json_format=None):
        """
        :type json_format: office365.runtime.odata.odata_json_format.ODataJsonFormat or None
        """
        json_items = [item for item in self._data]
        for i, v in enumerate(json_items):
            if isinstance(v, ClientValue):
                json_items[i] = v.to_json(json_format)
        if isinstance(json_format, JsonLightFormat) and json_format.is_verbose:
            json = {json_format.collection_tag_name: json_items,
                    json_format.metadata_type_tag_name: {'type': self.entity_type_name}}

            return json
        return json_items

    def set_property(self, index, value, persist_changes=False):
        child_value = self._item_type()
        if isinstance(child_value, ClientValue):
            for k, v in value.items():
                child_value.set_property(k, v, False)
        else:
            child_value = value
        self.add(child_value)

    @property
    def entity_type_name(self):
        """
        Gets server type name
        """
        primitive_types = {
            bool: "Edm.Boolean",
            int: "Edm.Int32",
            str: "Edm.String",
        }

        item_type_name = None

        is_primitive = primitive_types.get(self._item_type, None) is not None
        if is_primitive:
            item_type_name = primitive_types[self._item_type]
        elif issubclass(self._item_type, ClientValue):
            item_type_name = self._item_type.entity_type_name.fget(self)

        if item_type_name is not None:
            return "Collection({0})".format(item_type_name)
        else:
            return None
