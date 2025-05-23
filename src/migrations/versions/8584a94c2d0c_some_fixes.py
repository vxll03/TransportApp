"""some fixes

Revision ID: 8584a94c2d0c
Revises: 
Create Date: 2025-04-22 17:57:12.124274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8584a94c2d0c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bookings', 'booking_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    op.alter_column('bookings', 'departure_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    op.drop_constraint('bookings_user_id_fkey', 'bookings', type_='foreignkey')
    op.drop_constraint('bookings_route_id_fkey', 'bookings', type_='foreignkey')
    op.create_foreign_key(None, 'bookings', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'bookings', 'routes', ['route_id'], ['id'], ondelete='CASCADE')
    op.alter_column('routes', 'departure_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('routes', 'departure_date',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.drop_constraint(None, 'bookings', type_='foreignkey')
    op.drop_constraint(None, 'bookings', type_='foreignkey')
    op.create_foreign_key('bookings_route_id_fkey', 'bookings', 'routes', ['route_id'], ['id'])
    op.create_foreign_key('bookings_user_id_fkey', 'bookings', 'users', ['user_id'], ['id'])
    op.alter_column('bookings', 'departure_date',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.alter_column('bookings', 'booking_date',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    # ### end Alembic commands ###
