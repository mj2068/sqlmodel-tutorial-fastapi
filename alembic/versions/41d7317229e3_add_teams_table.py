"""add teams table

Revision ID: 41d7317229e3
Revises: f6905c445090
Create Date: 2023-08-19 14:52:57.519998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


#
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '41d7317229e3'
down_revision: Union[str, None] = 'f6905c445090'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teams',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('headquarters', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teams')
    # ### end Alembic commands ###
