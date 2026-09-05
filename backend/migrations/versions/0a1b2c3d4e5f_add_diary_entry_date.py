"""add diary entry_date

Revision ID: 0a1b2c3d4e5f
Revises: f7a8b9c0d1e2
Create Date: 2026-09-05

"""
from alembic import op
import sqlalchemy as sa


revision = '0a1b2c3d4e5f'
down_revision = 'f7a8b9c0d1e2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('diaries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('entry_date', sa.Date(), nullable=True))
        batch_op.create_index(batch_op.f('ix_diaries_entry_date'), ['entry_date'], unique=False)


def downgrade():
    with op.batch_alter_table('diaries', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_diaries_entry_date'))
        batch_op.drop_column('entry_date')
