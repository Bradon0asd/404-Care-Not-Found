"""align diary and note tables with models

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-09-05 10:30:00.000000

The 381c887fca9b revision was stamped without its DDL being applied, so the
database still carries the older diary_entries / notes shape. Both tables are
empty, so the drift is corrected by rebuilding rather than by migrating data.

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2c3d4e5f6a7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('diary_entries')
    op.create_table(
        'diaries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_private', sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_diaries_creator_id'), 'diaries', ['creator_id'], unique=False)

    op.add_column('notes', sa.Column('images', sa.JSON(), nullable=False))
    op.add_column(
        'notes',
        sa.Column('is_private', sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.alter_column(
        'notes',
        'is_reviewed',
        existing_type=sa.Boolean(),
        server_default=sa.false(),
        nullable=False,
    )
    op.drop_column('notes', 'is_read')
    op.create_index(op.f('ix_notes_creator_id'), 'notes', ['creator_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_notes_creator_id'), table_name='notes')
    op.add_column('notes', sa.Column('is_read', sa.Boolean(), nullable=True))
    op.alter_column(
        'notes',
        'is_reviewed',
        existing_type=sa.Boolean(),
        server_default=None,
        nullable=True,
    )
    op.drop_column('notes', 'is_private')
    op.drop_column('notes', 'images')

    op.drop_index(op.f('ix_diaries_creator_id'), table_name='diaries')
    op.drop_table('diaries')
    op.create_table(
        'diary_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('images', sa.JSON(), nullable=False),
        sa.Column('is_private', sa.Boolean(), nullable=True),
        sa.Column('ai_analysis', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
