"""add heroes table

Revision ID: f6905c445090
Revises: 
Create Date: 2023-08-19 00:12:21.239706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


#
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "f6905c445090"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "heroes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("secret_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("heroes")
    # ### end Alembic commands ###
