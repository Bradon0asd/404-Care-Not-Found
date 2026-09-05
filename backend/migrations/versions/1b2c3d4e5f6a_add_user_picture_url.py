"""add users.picture_url

Revision ID: 1b2c3d4e5f6a
Revises: f7a8b9c0d1e2
Create Date: 2026-09-05

"""
from alembic import op
import sqlalchemy as sa


revision = '1b2c3d4e5f6a'
down_revision = 'f7a8b9c0d1e2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_url', sa.String(length=512), nullable=True))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('picture_url')
