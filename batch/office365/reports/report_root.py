from office365.entity import Entity
from office365.reports.internal.queries.create_report_query import create_report_query


class ReportRoot(Entity):
    """The resource that represents an instance of History Reports."""

    def get_email_activity_counts(self, period):
        """
        Enables you to understand the trends of email activity (like how many were sent, read, and received)
        in your organization.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """

        qry = create_report_query(self, "getEmailActivityCounts", period)
        self.context.add_query(qry)
        return qry.return_type

    def get_email_activity_user_counts(self, period):
        """
        Enables you to understand trends on the number of unique users who are performing email activities
        like send, read, and receive.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        qry = create_report_query(self, "getEmailActivityUserCounts", period)
        self.context.add_query(qry)
        return qry.return_type

    def get_office365_activations_user_counts(self):
        """
        Get the count of Microsoft 365 activations on desktops and devices.

        """
        qry = create_report_query(self, "getOffice365ActivationsUserCounts")
        self.context.add_query(qry)
        return qry.return_type

    def get_onedrive_activity_file_counts(self, period):
        """
        Get the number of unique, licensed users that performed file interactions against any OneDrive account.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        qry = create_report_query(self, "getOneDriveActivityFileCounts", period)
        self.context.add_query(qry)
        return qry.return_type

    def get_onedrive_activity_user_counts(self, period):
        """
        Get the trend in the number of active OneDrive users.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        qry = create_report_query(self, "getOneDriveActivityUserCounts", period)
        self.context.add_query(qry)
        return qry.return_type

    def get_onedrive_activity_user_detail(self, period):
        """
        Get details about OneDrive activity by user.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        qry = create_report_query(self, "getOneDriveActivityUserDetail", period)
        self.context.add_query(qry)
        return qry.return_type

    def get_onedrive_usage_file_counts(self, period):
        """
        Get the total number of files across all sites and how many are active files. A file is considered active
        if it has been saved, synced, modified, or shared within the specified time period.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        qry = create_report_query(self, "getOneDriveUsageFileCounts", period)
        self.context.add_query(qry)
        return qry.return_type

    def get_onedrive_usage_storage(self, period):
        """
        Get the trend on the amount of storage you are using in OneDrive for Business.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        qry = create_report_query(self, "getOneDriveUsageStorage", period)
        self.context.add_query(qry)
        return qry.return_type

    def get_sharepoint_activity_pages(self, period):
        """
        Get the number of unique pages visited by users.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        qry = create_report_query(self, "getSharePointActivityPages", period)
        self.context.add_query(qry)
        return qry.return_type

    def get_sharepoint_activity_user_counts(self, period):
        """
        Get the trend in the number of active users. A user is considered active if he or she has executed a
        file activity (save, sync, modify, or share) or visited a page within the specified time period.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        qry = create_report_query(self, "getSharePointActivityUserCounts", period)
        self.context.add_query(qry)
        return qry.return_type

    def get_sharepoint_activity_user_detail(self, period):
        """
        Get details about SharePoint activity by user.

        :param str period: Specifies the length of time over which the report is aggregated.
            The supported values for {period_value} are: D7, D30, D90, and D180. These values follow the format
            Dn where n represents the number of days over which the report is aggregated. Required.
        """
        qry = create_report_query(self, "getSharePointActivityUserDetail", period)
        self.context.add_query(qry)
        return qry.return_type
