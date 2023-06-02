
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
                "name": "SampleTable",
                "fields": {
                    "id": {"column_type": "int4", "unique_id": 123},
                    "name": {"column_type": "text", "unique_id": 456}
                }
            }
        }
    ]
    migration_file.write(bytes(json.dumps(content), 'utf-8'))
    migration_file.seek(0)
    response = await migrator.create_script(
        migration_file=migration_file.name,
        table_name="sample_table"
    )
    expected = ["CREATE TABLE sample_table (id int4,name text)"]
    assert response == expected


@pytest.mark.asyncio
async def test_create_script_add_column():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file has two entries -> should create table and add a column
    content = [
        {
            "model": {
                "name": "SampleTable",
                "fields": {
                    "id": {"column_type": "int4", "unique_id": 123},
                    "name": {"column_type": "text", "unique_id": 456}
                }
            }
        },
        {
            "model": {
                "name": "SampleTable",
                "fields": {
                    "id": {"column_type": "int4", "unique_id": 123},
                    "name": {"column_type": "text", "unique_id": 456},
                    "last_name": {"column_type": "text", "unique_id": 999},
                    "age": {"column_type": "int2", "unique_id": 222}
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
        expected = "ALTER TABLE new_table ADD age int2,last_name text"
        assert response[1] == expected


@pytest.mark.asyncio
async def test_create_script_remove_column():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file has two entries -> should create table and remove a column
    content = [
        {
            "model": {
                "name": "SampleTable",
                "fields": {
                    "id": {"column_type": "int4", "unique_id": 123},
                    "name": {"column_type": "text", "unique_id": 456},
                    "age": {"column_type": "int2", "unique_id": 222}
                }
            }
        },
        {
            "model": {
                "name": "SampleTable",
                "fields": {
                    "id": {"column_type": "int4", "unique_id": 123},
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
        expected = "ALTER TABLE new_table DROP COLUMN age,name"
        assert response[1] == expected


@pytest.mark.asyncio
async def test_create_script_update_column():
    migrator = Migrator()
    migration_file = tempfile.NamedTemporaryFile()

    # Migration file has two entries -> should create table and update two columns
    content = [
        {
            "model": {
                "name": "SampleTable",
                "fields": {
                    "id": {"column_type": "int4", "unique_id": 123},
                    "name": {"column_type": "varchar(255)", "unique_id": 456}
                }
            }
        },
        {
            "model": {
                "name": "SampleTable",
                "fields": {
                    "id": {"column_type": "float4", "unique_id": 123},
                    "name": {"column_type": "text", "unique_id": 456},
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
        expected = "ALTER TABLE new_table ALTER COLUMN id float4,name text"
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
                "name": "SampleTable",
                "fields": {
                    "id": {"column_type": "int4", "unique_id": 123},
                    "name": {"column_type": "varchar(255)", "unique_id": 456}
                }
            }
        },
        {
            "model": {
                "name": "SampleTable",
                "fields": {
                    "id": {"column_type": "float4", "unique_id": 123},
                    "last_name": {"column_type": "text", "unique_id": 999},
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
        expected_add = "ALTER TABLE new_table ADD last_name text"
        expected_remove = "ALTER TABLE new_table DROP COLUMN name"
        expected_change = "ALTER TABLE new_table ALTER COLUMN id float4"
        assert len(response) == 4, "Should have one query for creation and three for updating"
        assert response[1] == expected_add
        assert response[2] == expected_remove
        assert response[3] == expected_change


@pytest.mark.asyncio
async def test_calculate_delta_new_fields():
    migrator = Migrator()
    # New fields
    old_model = {
        "fields": {
            "id": {
                "column_type": "int4"
            }
        }
    }
    new_model = {
        "fields": {
            "id": {
                "column_type": "int4"
            },
            "name": {
                "column_type": "text"
            },
            "amount": {
                "column_type": "float4"
            }
        }
    }
    response = await migrator.calculate_delta(old_model, new_model)
    expected = {
        "add": {
            "name": {
                "column_type": "text"
            },
            "amount": {
                "column_type": "float4"
            }
        },
        "remove": {},
        "update": {}
    }
    assert response == expected


@pytest.mark.asyncio
async def test_calculate_delta_delete_fields():
    migrator = Migrator()
    # Remove fields
    old_model = {
        "fields": {
            "id": {
                "column_type": "int4"
            },
            "name": {
                "column_type": "text"
            },
            "amount": {
                "column_type": "float4"
            }
        }
    }
    new_model = {
        "fields": {
            "id": {
                "column_type": "int4"
            }
        }
    }
    response = await migrator.calculate_delta(old_model, new_model)
    expected = {
        "remove": {
            "name": {
                "column_type": "text"
            },
            "amount": {
                "column_type": "float4"
            }
        },
        "add": {},
        "update": {}
    }
    assert response == expected


@pytest.mark.asyncio
async def test_calculate_delta_update_fields():
    migrator = Migrator()
    # Update fields
    old_model = {
        "fields": {
            "id": {
                "column_type": "int4"
            },
            "name": {
                "column_type": "text"
            },
            "amount": {
                "column_type": "float4"
            }
        }
    }
    new_model = {
        "fields": {
            "id": {
                "column_type": "text"
            },
            "name": {
                "column_type": "int4"
            },
            "amount": {
                "column_type": "float4"
            }
        }
    }
    response = await migrator.calculate_delta(old_model, new_model)
    expected = {
        "update": {
            "id": {
                "column_type": "text"
            },
            "name": {
                "column_type": "int4"
            },
        },
        "add": {},
        "remove": {}
    }
    assert response == expected
