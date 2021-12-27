from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.queries.service_operation_query import ServiceOperationQuery
from office365.runtime.paths.resource_path import ResourcePath
from office365.teams.channels.channel import Channel
from office365.teams.channels.channel_collection import ChannelCollection
from office365.teams.shifts.schedule import Schedule
from office365.teams.team_fun_settings import TeamFunSettings
from office365.teams.team_guest_settings import TeamGuestSettings
from office365.teams.team_member_settings import TeamMemberSettings
from office365.teams.team_messaging_settings import TeamMessagingSettings
from office365.teams.apps.teams_app_installation import TeamsAppInstallation
from office365.teams.operations.teams_async_operation import TeamsAsyncOperation
from office365.teams.teams_template import TeamsTemplate


class Team(Entity):
    """A team in Microsoft Teams is a collection of channel objects. A channel represents a topic, and therefore a
    logical isolation of discussion, within a team. """

    def delete_object(self):
        def _team_loaded():
            group = self.context.groups[self.id]
            group.delete_object(False)

        self.ensure_property("id", _team_loaded)
        return self

    @property
    def fun_settings(self):
        """Settings to configure use of Giphy, memes, and stickers in the team."""
        return self.properties.get('funSettings', TeamFunSettings())

    @property
    def member_settings(self):
        """Settings to configure whether members can perform certain actions, for example,
        create channels and add bots, in the team."""
        return self.properties.get('memberSettings', TeamMemberSettings())

    @property
    def guest_settings(self):
        """Settings to configure whether guests can create, update, or delete channels in the team."""
        return self.properties.get('guestSettings', TeamGuestSettings())

    @property
    def messaging_settings(self):
        """Settings to configure messaging and mentions in the team."""
        return self.properties.get('guestSettings', TeamMessagingSettings())

    @property
    def display_name(self):
        """The name of the team.

        :rtype: str or None
        """
        return self.properties.get('displayName', None)

    @property
    def description(self):
        """An optional description for the team.

        :rtype: str or None
        """
        return self.properties.get('description', None)

    @property
    def classification(self):
        """An optional label. Typically describes the data or business sensitivity of the team.
        Must match one of a pre-configured set in the tenant's directory.

        :rtype: str or None
        """
        return self.properties.get('classification', None)

    @property
    def is_archived(self):
        """Whether this team is in read-only mode."""
        return self.properties.get('isArchived', None)

    @property
    def visibility(self):
        """The visibility of the group and team. Defaults to Public."""
        return self.properties.get('visibility', None)

    @property
    def web_url(self):
        """A hyperlink that will go to the team in the Microsoft Teams client. This is the URL that you get when
        you right-click a team in the Microsoft Teams client and select Get link to team. This URL should be treated
        as an opaque blob, and not parsed."""
        return self.properties.get('webUrl', None)

    @property
    def created_datetime(self):
        """Timestamp at which the team was created."""
        return self.properties.get('createdDateTime', None)

    @property
    def channels(self):
        """The collection of channels & messages associated with the team.

        :rtype: ChannelCollection
        """
        return self.get_property('channels',
                                 ChannelCollection(self.context, ResourcePath("channels", self.resource_path)))

    @property
    def group(self):
        """"""
        from office365.directory.groups.group import Group
        return self.properties.get("group", Group(self.context, ResourcePath("group", self.resource_path)))

    @property
    def primary_channel(self):
        """
        The general channel for the team.

        :rtype: Channel
        """
        return self.get_property('primaryChannel',
                                 Channel(self.context, ResourcePath("primaryChannel", self.resource_path)))

    @property
    def schedule(self):
        """The shifts of shifts for this team.

        :rtype: Schedule
        """
        return self.get_property('shifts',
                                 Schedule(self.context, ResourcePath("shifts", self.resource_path)))

    @property
    def installed_apps(self):
        """The apps installed in this team.

        :rtype: EntityCollection
        """
        return self.get_property('installedApps',
                                 EntityCollection(self.context, TeamsAppInstallation,
                                                  ResourcePath("installedApps", self.resource_path)))

    @property
    def operations(self):
        """The async operations that ran or are running on this team.

        :rtype: EntityCollection
        """
        return self.get_property('operations',
                                 EntityCollection(self.context, TeamsAsyncOperation,
                                                  ResourcePath("installedApps", self.resource_path)))

    @property
    def template(self):
        """The template this team was created from

        :rtype: TeamsTemplate
        """
        return self.get_property('template',
                                 TeamsTemplate(self.context, ResourcePath("template", self.resource_path)))

    def archive(self):
        """Archive the specified team. When a team is archived, users can no longer send or like messages on any
        channel in the team, edit the team's name, description, or other settings, or in general make most changes to
        the team. Membership changes to the team continue to be allowed. """
        qry = ServiceOperationQuery(self, "archive")
        self.context.add_query(qry)
        return self

    def unarchive(self):
        """Restore an archived team. This restores users' ability to send messages and edit the team, abiding by
        tenant and team settings. """
        qry = ServiceOperationQuery(self, "unarchive")
        self.context.add_query(qry)
        return self

    def clone(self):
        """Create a copy of a team. This operation also creates a copy of the corresponding group. """
        qry = ServiceOperationQuery(self, "clone")
        self.context.add_query(qry)
        return self

    def send_activity_notification(self, topic, activity_type, chain_id, preview_text, template_parameters, recipient):
        """
        Send an activity feed notification in the scope of a team.
        For more details about sending notifications and the requirements for doing so,
        see sending Teams activity notifications:
        https://docs.microsoft.com/en-us/graph/teams-send-activityfeednotifications

        """
        payload = {
            "topic": topic,
            "activityType": activity_type,
            "chainId": chain_id,
            "previewText": preview_text,
            "templateParameters": template_parameters,
            "recipient": recipient
        }
        qry = ServiceOperationQuery(self, "sendActivityNotification", None, payload)
        self.context.add_query(qry)
        return self

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "installedApps": self.installed_apps,
                "primaryChannel": self.primary_channel
            }
            default_value = property_mapping.get(name, None)
        return super(Team, self).get_property(name, default_value)

    def set_property(self, name, value, persist_changes=True):
        super(Team, self).set_property(name, value, persist_changes)
        # fallback: determine whether resource path is resolved
        if name == "id" and self._resource_path.name == "team":
            self._resource_path = ResourcePath(value, ResourcePath("teams"))
        return self
