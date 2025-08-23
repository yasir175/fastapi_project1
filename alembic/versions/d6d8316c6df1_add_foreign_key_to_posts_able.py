"""add foreign key to posts able

Revision ID: d6d8316c6df1
Revises: 376999329b49
Create Date: 2025-08-22 23:59:45.903656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6d8316c6df1'
down_revision: Union[str, Sequence[str], None] = '376999329b49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",
                          local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")


def downgrade():
    op.drop_constraint("posts_users_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    
