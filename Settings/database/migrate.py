import traceback
from typing import List, Tuple, Dict

import yaml
from mongoengine.context_managers import switch_db

from configs import project_root
from database import db_connections
from database.models.tags import TagModel, TagsModel
from modules.utils import log


def get_migrations() -> List[Tuple[str, Dict]]:
    """Get all migrations.

    Returns:
        List[Tuple[str, Dict]]: List with migration file name and it's contents.
    """
    migration_folder = project_root.joinpath('database').joinpath('migrations')

    migration_data = []

    for migration_file in migration_folder.glob('*.yaml'):
        with open(migration_file) as file:
            for data in yaml.load_all(file, yaml.Loader):
                migration_data.append((migration_file, data))

    return migration_data


def migrate() -> None:
    """Run migrations.
    """
    migrations = get_migrations()

    for migration_file, migration_data in migrations:
        database = migration_data.get('database')
        documents = migration_data.get('documents')

        # Check if database and documents exists in migration.
        if database and documents:
            db_alias = db_connections.get(database)

            if db_alias is None:
                log('error', f'Unable to migrate "{migration_file.name}".',
                    f'Reason: There is no connection to database "{database}", check the configs.')
            else:
                for document in documents:
                    server = document.get('server')
                    tags = document.get('tags')

                    tag_list = []

                    for tag in tags:
                        tag_id = tag.get('id')
                        tag_name = tag.get('name')
                        tag_system = tag.get('system')
                        tag_status = tag.get('status')
                        tag_const = tag.get('const')
                        tag_mv = tag.get('mv')

                        tag_list.append(
                            TagModel(
                                tag_id=tag_id,
                                tag_name=tag_name,
                                tag_system = tag_system,
                                tag_status = tag_status,
                                tag_const = tag_const,
                                tag_mv = tag_mv
                            )
                        )

                    with switch_db(TagsModel, db_alias) as tags_model:
                        try:
                            tags_model(server=server, tags=tag_list).save()

                            log('info', f'Migrated "{migration_file.name}".')
                        except Exception:
                            log('error', f'There was a problem migrating "{migration_file.name}".',
                                traceback.format_exc())
