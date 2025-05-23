"""created another tables

Revision ID: dc763715a132
Revises: 94d0831616b3
Create Date: 2025-04-21 21:02:03.305425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc763715a132'
down_revision: Union[str, None] = '94d0831616b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('departure_place', sa.String(), nullable=False),
    sa.Column('arrival_place', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('departure_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('booking_date', sa.DateTime(), nullable=False),
    sa.Column('departure_date', sa.DateTime(), nullable=False),
    sa.Column('state', sa.Enum('booked', 'cancelled', 'passed', name='state'), nullable=False),
    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    op.drop_table('routes')
    # ### end Alembic commands ###
