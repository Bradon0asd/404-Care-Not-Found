"""add care schedules and vital sign logs

Revision ID: a1b2c3d4e5f6
Revises: 381c887fca9b
Create Date: 2026-09-04 21:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '381c887fca9b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'care_schedules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('care_recipient_id', sa.Integer(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('schedule_type', sa.String(length=20), nullable=False),
        sa.Column('weekday', sa.Integer(), nullable=True),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint("schedule_type IN ('weekday', 'weekend')", name='ck_care_schedules_schedule_type'),
        sa.ForeignKeyConstraint(['care_recipient_id'], ['care_recipients.id'], ),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_care_schedules_care_recipient_id'),
        'care_schedules',
        ['care_recipient_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_care_schedules_creator_id'),
        'care_schedules',
        ['creator_id'],
        unique=False,
    )
    op.create_table(
        'vital_sign_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('care_recipient_id', sa.Integer(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('vital_type', sa.String(length=30), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('secondary_value', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('measured_at', sa.DateTime(), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['care_recipient_id'], ['care_recipients.id'], ),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_vital_sign_logs_care_recipient_id'),
        'vital_sign_logs',
        ['care_recipient_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_vital_sign_logs_creator_id'),
        'vital_sign_logs',
        ['creator_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_vital_sign_logs_measured_at'),
        'vital_sign_logs',
        ['measured_at'],
        unique=False,
    )
    op.create_index(
        op.f('ix_vital_sign_logs_vital_type'),
        'vital_sign_logs',
        ['vital_type'],
        unique=False,
    )


def downgrade():
    op.drop_index(op.f('ix_vital_sign_logs_vital_type'), table_name='vital_sign_logs')
    op.drop_index(op.f('ix_vital_sign_logs_measured_at'), table_name='vital_sign_logs')
    op.drop_index(op.f('ix_vital_sign_logs_creator_id'), table_name='vital_sign_logs')
    op.drop_index(op.f('ix_vital_sign_logs_care_recipient_id'), table_name='vital_sign_logs')
    op.drop_table('vital_sign_logs')
    op.drop_index(op.f('ix_care_schedules_creator_id'), table_name='care_schedules')
    op.drop_index(op.f('ix_care_schedules_care_recipient_id'), table_name='care_schedules')
    op.drop_table('care_schedules')
