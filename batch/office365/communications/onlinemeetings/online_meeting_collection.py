from office365.communications.onlinemeetings.online_meeting import OnlineMeeting
from office365.entity_collection import EntityCollection
from office365.runtime.queries.create_entity_query import CreateEntityQuery
from office365.runtime.queries.service_operation_query import ServiceOperationQuery


class OnlineMeetingCollection(EntityCollection):

    def __init__(self, context, resource_path=None):
        super(OnlineMeetingCollection, self).__init__(context, OnlineMeeting, resource_path)

    def create(self, subject, start_datetime=None, end_datetime=None):
        """
        Create an online meeting on behalf of a user by using the object ID (OID) in the user token.

        :param datetime.datetime start_datetime: The meeting start time in UTC.
        :param datetime.datetime end_datetime: The meeting end time in UTC.
        :param str subject: The subject of the online meeting.
        """
        return_type = OnlineMeeting(self.context)
        self.add_child(return_type)
        payload = {
            "startDateTime": start_datetime,
            "endDateTime": end_datetime,
            "subject": subject,
        }
        qry = CreateEntityQuery(self, payload, return_type)
        self.context.add_query(qry)
        return return_type

    def create_or_get(self, external_id=None, start_datetime=None, end_datetime=None, subject=None, participants=None,
                      chat_info=None):
        """Create an onlineMeeting object with a custom specified external ID. If the external ID already exists,
        this API will return the onlineMeeting object with that external ID.

        :param str external_id: The external ID. A custom ID. (Required)
        :param datetime.datetime start_datetime: The meeting start time in UTC.
        :param datetime.datetime end_datetime: The meeting end time in UTC.
        :param str subject: The subject of the online meeting.
        :param MeetingParticipants participants: The participants associated with the online meeting.
             This includes the organizer and the attendees.

        :param ChatInfo chat_info:
        """
        return_type = OnlineMeeting(self.context)
        self.add_child(return_type)
        payload = {
            "externalId": external_id,
            "startDateTime": start_datetime,
            "endDateTime": end_datetime,
            "subject": subject,
            "chatInfo": chat_info,
            "participants": participants
        }
        qry = ServiceOperationQuery(self, "createOrGet", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type
