"""add invites

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-09-05 14:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd4e5f6a7b8c9'
down_revision = 'c3d4e5f6a7b8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'invites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=64), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('nurse_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['nurse_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('invites', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_invites_code'), ['code'], unique=True)
        batch_op.create_index(batch_op.f('ix_invites_owner_id'), ['owner_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_invites_nurse_id'), ['nurse_id'], unique=False)


def downgrade():
    with op.batch_alter_table('invites', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_invites_nurse_id'))
        batch_op.drop_index(batch_op.f('ix_invites_owner_id'))
        batch_op.drop_index(batch_op.f('ix_invites_code'))

    op.drop_table('invites')
