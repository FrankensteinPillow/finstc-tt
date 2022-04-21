"""init

Revision ID: 19348b5ed48a
Revises:
Create Date: 2022-04-20 16:16:30.180683

"""
import uuid

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "19348b5ed48a"
down_revision = None
branch_labels = None
depends_on = None

TEST_DILLERS = [
    {
        "id": uuid.uuid4().hex,
        "company_name": "Auto House",
        "address": "USA, New York",
    },
    {
        "id": uuid.uuid4().hex,
        "company_name": "Maschinenhäuser",
        "address": "Germany, Berlin",
    },
]
TEST_VEHICLES = [
    {
        "id": uuid.uuid4().hex,
        "brand": "BMW",
        "model": "X6",
        "vin": "FB9D3393FEB1455D",
        "colour": "black",
        "year": "2022",
        "diller_id": TEST_DILLERS[0]["id"],
    },
    {
        "id": uuid.uuid4().hex,
        "brand": "KIA",
        "model": "Rio",
        "vin": "96A857233CCD471E",
        "colour": "white",
        "year": "2018",
        "diller_id": TEST_DILLERS[1]["id"],
    },
    {
        "id": uuid.uuid4().hex,
        "brand": "Opel",
        "model": "Astra GTC",
        "vin": "3E1711DD2C1446D4",
        "colour": "yellow",
        "year": "2021",
        "diller_id": TEST_DILLERS[0]["id"],
    },
    {
        "id": uuid.uuid4().hex,
        "brand": "KIA",
        "model": "K5",
        "vin": "0C92574CECDA42E4",
        "colour": "grey",
        "year": "2020",
        "diller_id": TEST_DILLERS[1]["id"],
    },
]


def upgrade():
    op.drop_table("vehicles")
    op.drop_table("dillers")
    dillers = op.create_table(
        "dillers",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("company_name", sa.Text),
        sa.Column("address", sa.Text),
    )
    vehicles = op.create_table(
        "vehicles",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("brand", sa.Text),
        sa.Column("model", sa.Text),
        sa.Column("vin", sa.Text, unique=True, nullable=False),
        sa.Column("colour", sa.Text),
        sa.Column("year", sa.Integer),
        sa.Column(
            "diller_id",
            sa.String(length=32),
            sa.ForeignKey("dillers.id", name="fk_vehicles_dillers_id"),
            nullable=False,
        ),
    )
    op.bulk_insert(dillers, TEST_DILLERS)
    op.bulk_insert(vehicles, TEST_VEHICLES)


def downgrade():
    op.drop_table("vehicles")
    op.drop_table("dillers")
