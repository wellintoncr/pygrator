
import json
import tempfile
from unittest import mock


from migrator import Migrator

import pytest


@pytest.mark.asyncio
async def test_create_script_do_nothing():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file is empty -> should do nothing
    migration_file.write(b'')
    response = await migrator.create_script(
        migration_file=migration_file.name,
        table_name="new_table"
    )
    assert response is None

    # Migration file is empty list -> should do nothing
    migration_file.write(b'[]')
    migration_file.seek(0)
    response = await migrator.create_script(
        migration_file=migration_file.name,
        table_name="new_table"
    )
    assert response is None


@pytest.mark.asyncio
async def test_create_script_create_table():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file has one entry -> should create table
    content = [
        {
            "model": {
                "id": {
                    "field_type": "<type Integer>"
                },
                "name": {
                    "field_type": "<type String>"
                }
            }
        }
    ]
    migration_file.write(bytes(json.dumps(content), 'utf-8'))
    migration_file.seek(0)
    response = await migrator.create_script(
        migration_file=migration_file.name,
        table_name="new_table"
    )
    expected = ["CREATE TABLE new_table (id INT,name VARCHAR(255))"]
    assert response == expected


@pytest.mark.asyncio
async def test_create_script_add_column():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file has two entries -> should create table and add a column
    content = [
        {
            "model": {
                "id": {
                    "field_type": "<type Integer>"
                },
                "name": {
                    "field_type": "<type String>"
                }
            }
        },
        {
            "model": {
                "id": {
                    "field_type": "<type Integer>"
                },
                "name": {
                    "field_type": "<type String>"
                },
                "amount": {
                    "field_type": "<type Float>"
                },
                "surname": {
                    "field_type": "<type String>"
                }
            }
        }
    ]
    migration_file.write(bytes(json.dumps(content), 'utf-8'))
    migration_file.seek(0)
    with mock.patch("migrator.Migrator.create_table") as create_table_mock:
        create_table_mock.return_value = ["mock"]
        response = await migrator.create_script(
            migration_file=migration_file.name,
            table_name="new_table"
        )
        expected = "ALTER TABLE new_table ADD amount DECIMAL(10,2),surname VARCHAR(255)"
        assert response[1] == expected


@pytest.mark.asyncio
async def test_create_script_remove_column():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file has two entries -> should create table and remove a column
    content = [
        {
            "model": {
                "id": {
                    "field_type": "<type Integer>"
                },
                "name": {
                    "field_type": "<type String>"
                },
                "amount": {
                    "field_type": "<type Float>"
                },
                "surname": {
                    "field_type": "<type String>"
                }
            }
        },
        {
            "model": {
                "id": {
                    "field_type": "<type Integer>"
                },
                "name": {
                    "field_type": "<type String>"
                }
            }
        }
    ]
    migration_file.write(bytes(json.dumps(content), 'utf-8'))
    migration_file.seek(0)
    with mock.patch("migrator.Migrator.create_table") as create_table_mock:
        create_table_mock.return_value = ["mock"]
        response = await migrator.create_script(
            migration_file=migration_file.name,
            table_name="new_table"
        )
        expected = "ALTER TABLE new_table DROP COLUMN amount,surname"
        assert response[1] == expected


@pytest.mark.asyncio
async def test_create_script_update_column():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file has two entries -> should create table and update two columns
    content = [
        {
            "model": {
                "id": {
                    "field_type": "<type Integer>"
                },
                "name": {
                    "field_type": "<type String>"
                },
                "amount": {
                    "field_type": "<type Float>"
                }
            }
        },
        {
            "model": {
                "id": {
                    "field_type": "<type String>"
                },
                "name": {
                    "field_type": "<type Float>"
                },
                "amount": {
                    "field_type": "<type Float>"
                }
            }
        }
    ]
    migration_file.write(bytes(json.dumps(content), 'utf-8'))
    migration_file.seek(0)
    with mock.patch("migrator.Migrator.create_table") as create_table_mock:
        create_table_mock.return_value = ["mock"]
        response = await migrator.create_script(
            migration_file=migration_file.name,
            table_name="new_table"
        )
        expected = "ALTER TABLE new_table ALTER COLUMN id VARCHAR(255),name DECIMAL(10,2)"
        assert response[1] == expected


@pytest.mark.asyncio
async def test_create_script_all_changes():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file has two entries -> should create table and
    # add column, remove column and change column type
    content = [
        {
            "model": {
                "id": {
                    "field_type": "<type Integer>"
                },
                "name": {
                    "field_type": "<type String>"
                }
            }
        },
        {
            "model": {
                "id": {
                    "field_type": "<type String>"
                },
                "amount": {
                    "field_type": "<type Float>"
                }
            }
        }
    ]
    migration_file.write(bytes(json.dumps(content), 'utf-8'))
    migration_file.seek(0)
    with mock.patch("migrator.Migrator.create_table") as create_table_mock:
        create_table_mock.return_value = ["mock"]
        response = await migrator.create_script(
            migration_file=migration_file.name,
            table_name="new_table"
        )
        expected_add = "ALTER TABLE new_table ADD amount DECIMAL(10,2)"
        expected_remove = "ALTER TABLE new_table DROP COLUMN name"
        expected_change = "ALTER TABLE new_table ALTER COLUMN id VARCHAR(255)"
        assert len(response) == 4, "Should have one query for creation and three for updating"
        assert response[1] == expected_add
        assert response[2] == expected_remove
        assert response[3] == expected_change


@pytest.mark.asyncio
async def test_calculate_delta_new_fields():
    migrator = Migrator()
    # New fields
    old_model = {
        "id": {
            "field_type": "<type Integer>"
        }
    }
    new_model = {
        "id": {
            "field_type": "<type Integer>"
        },
        "name": {
            "field_type": "<type String>"
        },
        "amount": {
            "field_type": "<type Float>"
        }
    }
    response = await migrator.calculate_delta(old_model, new_model)
    expected = {
        "add": {
            "name": {
                "field_type": "<type String>"
            },
            "amount": {
                "field_type": "<type Float>"
            }
        },
        "remove": {},
        "update": {}
    }
    assert response == expected


@pytest.mark.asyncio
async def test_calculate_delta_delete_fields():
    migrator = Migrator()
    # New fields
    old_model = {
        "id": {
            "field_type": "<type Integer>"
        },
        "name": {
            "field_type": "<type String>"
        },
        "amount": {
            "field_type": "<type Float>"
        }
    }
    new_model = {
        "id": {
            "field_type": "<type Integer>"
        }
    }
    response = await migrator.calculate_delta(old_model, new_model)
    expected = {
        "remove": {
            "name": {
                "field_type": "<type String>"
            },
            "amount": {
                "field_type": "<type Float>"
            }
        },
        "add": {},
        "update": {}
    }
    assert response == expected


@pytest.mark.asyncio
async def test_calculate_delta_update_fields():
    migrator = Migrator()
    # New fields
    old_model = {
        "id": {
            "field_type": "<type Integer>"
        },
        "name": {
            "field_type": "<type String>"
        },
        "amount": {
            "field_type": "<type Float>"
        }
    }
    new_model = {
        "id": {
            "field_type": "<type String>"
        },
        "name": {
            "field_type": "<type Float>"
        },
        "amount": {
            "field_type": "<type Float>"
        }
    }
    response = await migrator.calculate_delta(old_model, new_model)
    expected = {
        "update": {
            "id": {
                "field_type": "<type String>"
            },
            "name": {
                "field_type": "<type Float>"
            },
        },
        "add": {},
        "remove": {}
    }
    assert response == expected
