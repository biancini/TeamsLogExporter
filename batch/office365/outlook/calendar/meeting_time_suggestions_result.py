from office365.outlook.calendar.meeting_time_suggestion import MeetingTimeSuggestion
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class MeetingTimeSuggestionsResult(ClientValue):
    """
    A collection of meeting suggestions if there is any, or the reason if there isn't.
    """
    def __init__(self, meetingTimeSuggestions=None,
                 emptySuggestionsReason=None):
        """

        :param ClientValueCollection(MeetingTimeSuggestion) meetingTimeSuggestions: An array of meeting suggestions.
        :param str emptySuggestionsReason: A reason for not returning any meeting suggestions.
            The possible values are: attendeesUnavailable, attendeesUnavailableOrUnknown, locationsUnavailable,
            organizerUnavailable, or unknown. This property is an empty string if the meetingTimeSuggestions property
            does include any meeting suggestions.
        """
        super(MeetingTimeSuggestionsResult, self).__init__()
        self.meetingTimeSuggestions = ClientValueCollection(MeetingTimeSuggestion) if meetingTimeSuggestions is None \
            else meetingTimeSuggestions
        self.emptySuggestionsReason = emptySuggestionsReason
