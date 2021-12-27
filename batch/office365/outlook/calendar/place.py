from office365.entity import Entity
from office365.outlook.mail.physical_address import PhysicalAddress


class Place(Entity):
    """Represents basic location attributes such as name, physical address, and geographic coordinates.
    This is the base type for richer location types such as room and roomList."""

    @property
    def address(self):
        """The street address of the place."""
        return self.properties.get("address", PhysicalAddress())

    @property
    def phone(self):
        """The phone number of the place."""
        return self.properties.get("phone", None)
