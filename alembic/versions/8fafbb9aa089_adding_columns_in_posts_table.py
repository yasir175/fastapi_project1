"""adding columns in posts table

Revision ID: 8fafbb9aa089
Revises: bf961d083f05
Create Date: 2025-08-22 23:50:21.913873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fafbb9aa089'
down_revision: Union[str, Sequence[str], None] = 'bf961d083f05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
