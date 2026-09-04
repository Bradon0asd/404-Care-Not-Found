"""add diary and sticky note

Revision ID: 381c887fca9b
Revises: 9f1d2c3b4a5e
Create Date: 2026-09-04 18:11:52.665246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '381c887fca9b'
down_revision = '9f1d2c3b4a5e'
branch_labels = None
depends_on = None


def upgrade():
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
    op.create_table(
        'notes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=30), nullable=True),
        sa.Column('priority', sa.String(length=20), server_default='normal', nullable=False),
        sa.Column('images', sa.JSON(), nullable=False),
        sa.Column('is_reviewed', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column('is_private', sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_notes_creator_id'), 'notes', ['creator_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_notes_creator_id'), table_name='notes')
    op.drop_table('notes')
    op.drop_index(op.f('ix_diaries_creator_id'), table_name='diaries')
    op.drop_table('diaries')
