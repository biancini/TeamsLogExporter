from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class TaxonomyFieldValue(ClientValue):

    def __init__(self, label=None, term_guid=None, wss_id=-1):
        """
        :type label: str
        :type term_guid: str
        """
        super(TaxonomyFieldValue, self).__init__()
        self.Label = label
        self.TermGuid = term_guid
        self.WssId = wss_id

    def __str__(self):
        return "{0};#{1}|{2}".format(self.WssId, self.Label, self.TermGuid)

    @property
    def entity_type_name(self):
        return "SP.Taxonomy.TaxonomyFieldValue"


class TaxonomyFieldValueCollection(ClientValueCollection):
    """Represents the multi-value object for the taxonomy column."""

    def __init__(self, initial_values):
        super(TaxonomyFieldValueCollection, self).__init__(TaxonomyFieldValue, initial_values)

    def __str__(self):
        return ";#".join([str(item) for item in self._data])
