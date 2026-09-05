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
    tables = _tables()
    if 'diary_entries' in tables:
        op.drop_table('diary_entries')

    if 'diaries' not in tables:
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

    if not _has_index('diaries', 'ix_diaries_creator_id'):
        op.create_index(op.f('ix_diaries_creator_id'), 'diaries', ['creator_id'], unique=False)

    note_columns = _columns('notes')
    if 'images' not in note_columns:
        op.add_column('notes', sa.Column('images', sa.JSON(), nullable=True))
        op.execute("UPDATE notes SET images = '[]' WHERE images IS NULL")
        op.alter_column('notes', 'images', existing_type=sa.JSON(), nullable=False)
    if 'is_private' not in note_columns:
        op.add_column(
            'notes',
            sa.Column('is_private', sa.Boolean(), server_default=sa.false(), nullable=False),
        )
    if 'is_reviewed' in note_columns:
        op.alter_column(
            'notes',
            'is_reviewed',
            existing_type=sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        )
    if 'is_read' in note_columns:
        op.drop_column('notes', 'is_read')
    if not _has_index('notes', 'ix_notes_creator_id'):
        op.create_index(op.f('ix_notes_creator_id'), 'notes', ['creator_id'], unique=False)


def downgrade():
    # This revision reconciles a stamped-but-not-applied shared database with the
    # clean migration chain. On a clean database most upgrade steps are no-ops, so
    # the downgrade must be conservative and avoid deleting tables/columns that
    # already belonged to earlier revisions.
    note_columns = _columns('notes')
    if 'is_reviewed' in note_columns:
        op.alter_column(
            'notes',
            'is_reviewed',
            existing_type=sa.Boolean(),
            server_default=None,
            nullable=True,
        )


def _inspector():
    return sa.inspect(op.get_bind())


def _tables():
    return set(_inspector().get_table_names())


def _columns(table_name):
    if table_name not in _tables():
        return set()
    return {column['name'] for column in _inspector().get_columns(table_name)}


def _has_index(table_name, index_name):
    if table_name not in _tables():
        return False
    return any(index['name'] == index_name for index in _inspector().get_indexes(table_name))
