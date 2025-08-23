"""creating users table

Revision ID: 376999329b49
Revises: 8fafbb9aa089
Create Date: 2025-08-22 23:50:43.117266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '376999329b49'
down_revision: Union[str, Sequence[str], None] = '8fafbb9aa089'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("users",
                    sa.Column("id",sa.Integer(),primary_key=True,nullable=False),
                    sa.Column("email",sa.String(),nullable=False,unique=True),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),
                                      nullable=False,server_default=sa.text('now()'))

                    )
    


def downgrade() :
    op.drop_table("users")
   
