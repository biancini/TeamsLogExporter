from office365.outlook.calendar.schedule_item import ScheduleItem
from office365.outlook.calendar.working_hours import WorkingHours
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class ScheduleInformation(ClientValue):
    """Represents the availability of a user, distribution list, or resource (room or equipment)
    for a specified time period."""

    def __init__(self, scheduleId=None, scheduleItems=None, availabilityView=None, error=None, workingHours=None):
        """

        :param WorkingHours workingHours: The days of the week and hours in a specific time zone that the user works.
             These are set as part of the user's mailboxSettings.
        :param str error: Error information from attempting to get the availability of the user, distribution list,
             or resource.
        :param str availabilityView: Represents a merged view of availability of all the items in scheduleItems.
             The view consists of time slots. Availability during each time slot is indicated with:
             0= free, 1= tentative, 2= busy, 3= out of office, 4= working elsewhere.
        :param ClientValueCollection(ScheduleItem) scheduleItems: Contains the items that describe the availability
            of the user or resource.
        :param str scheduleId: An SMTP address of the user, distribution list, or resource, identifying an instance
            of scheduleInformation.
        """
        super(ScheduleInformation, self).__init__()
        self.scheduleItems = ClientValueCollection(ScheduleItem) if scheduleItems is None else scheduleItems
        self.scheduleId = scheduleId
        self.availabilityView = availabilityView
        self.error = error
        self.workingHours = WorkingHours() if workingHours is None else workingHours
