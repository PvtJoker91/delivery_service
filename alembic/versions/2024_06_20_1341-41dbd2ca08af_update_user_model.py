"""update user model

Revision ID: 41dbd2ca08af
Revises: 7f1a28da392d
Create Date: 2024-06-20 13:41:01.754495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '41dbd2ca08af'
down_revision: Union[str, None] = '7f1a28da392d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=50), nullable=False))
    op.add_column('users', sa.Column('password', sa.String(length=50), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_name', mysql.VARCHAR(length=50), nullable=False))
    op.add_column('users', sa.Column('first_name', mysql.VARCHAR(length=50), nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'password')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###
