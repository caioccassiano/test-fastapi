"""add foreign key to posts

Revision ID: 0a28a532b92d
Revises: 3a9dbd2385fa
Create Date: 2025-03-25 10:02:16.928755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a28a532b92d'
down_revision: Union[str, None] = '3a9dbd2385fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Adiciona a coluna primeiro
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))

    # Depois cria a FK
    op.create_foreign_key(
        'post_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )

    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
