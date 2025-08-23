"""creating posts table

Revision ID: bf961d083f05
Revises: 
Create Date: 2025-08-22 23:45:40.516205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf961d083f05'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("posts",
                    sa.Column("id",sa.Integer(),primary_key=True,nullable=False),
                    sa.Column("title",sa.String(),nullable=False),
                    sa.Column("content",sa.String(),nullable=False),
                    sa.Column("published",sa.Boolean(),default=True),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),
                                      nullable=False,server_default=sa.text('now()'))

                    )
    

def downgrade():
    op.drop_table("posts")
