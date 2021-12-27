from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.planner.plans.plan import PlannerPlan
from office365.planner.tasks.task import PlannerTask
from office365.runtime.paths.resource_path import ResourcePath


class PlannerUser(Entity):
    """The plannerUser resource provide access to Planner resources for a user.
    It doesn't contain any usable properties."""

    @property
    def plans(self):
        """Read-only. Nullable. Returns the plannerTasks assigned to the user.

        :rtype: EntityCollection
        """
        return self.get_property('plans',
                                 EntityCollection(self.context, PlannerPlan,
                                                  ResourcePath("plans", self.resource_path)))

    @property
    def tasks(self):
        """Read-only. Nullable. Returns the plannerTasks assigned to the user.

        :rtype: EntityCollection
        """
        return self.get_property('tasks',
                                 EntityCollection(self.context, PlannerTask,
                                                  ResourcePath("tasks", self.resource_path)))
