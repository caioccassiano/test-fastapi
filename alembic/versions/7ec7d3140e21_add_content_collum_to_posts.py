"""add content collum to posts

Revision ID: 7ec7d3140e21
Revises: 0b729d50e262
Create Date: 2025-03-25 09:45:40.934685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ec7d3140e21'
down_revision: Union[str, None] = '0b729d50e262'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
