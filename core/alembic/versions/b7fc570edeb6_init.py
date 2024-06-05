"""init

Revision ID: b7fc570edeb6
Revises: 5bbb73878a70
Create Date: 2024-06-04 16:59:02.440344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7fc570edeb6'
down_revision: Union[str, None] = '5bbb73878a70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=30), nullable=False))
    op.drop_column('users', 'user_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_name', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_column('users', 'username')
    # ### end Alembic commands ###