import auditor

from db.getters.experiment_groups import get_running_experiment_group
from event_manager.events.experiment_group import (
    EXPERIMENT_GROUP_BO,
    EXPERIMENT_GROUP_GRID,
    EXPERIMENT_GROUP_HYPERBAND,
    EXPERIMENT_GROUP_RANDOM
)
from hpsearch.tasks import bo, grid, hyperband, random
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import HPCeleryTasks
from schemas.hptuning import SearchAlgorithms


@celery_app.task(name=HPCeleryTasks.HP_CREATE)
def hp_create(experiment_group_id):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id)
    create(experiment_group)


def create(experiment_group):
    if SearchAlgorithms.is_grid(experiment_group.search_algorithm):
        auditor.record(event_type=EXPERIMENT_GROUP_GRID,
                       instance=experiment_group)
        return grid.create(experiment_group=experiment_group)
    elif SearchAlgorithms.is_random(experiment_group.search_algorithm):
        auditor.record(event_type=EXPERIMENT_GROUP_RANDOM,
                       instance=experiment_group)
        return random.create(experiment_group=experiment_group)
    elif SearchAlgorithms.is_hyperband(experiment_group.search_algorithm):
        auditor.record(event_type=EXPERIMENT_GROUP_HYPERBAND,
                       instance=experiment_group)
        return hyperband.create(experiment_group=experiment_group)
    elif SearchAlgorithms.is_bo(experiment_group.search_algorithm):
        auditor.record(event_type=EXPERIMENT_GROUP_BO,
                       instance=experiment_group)
        return bo.create(experiment_group=experiment_group)
    return None
