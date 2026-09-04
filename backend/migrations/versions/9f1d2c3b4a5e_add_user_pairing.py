"""add user pairing

Revision ID: 9f1d2c3b4a5e
Revises: be52a55336ad
Create Date: 2026-09-04 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9f1d2c3b4a5e"
down_revision = "be52a55336ad"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("pair_user_id", sa.Integer(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_users_pair_user_id"),
            ["pair_user_id"],
            unique=True,
        )
        batch_op.create_foreign_key(
            "fk_users_pair_user_id_users",
            "users",
            ["pair_user_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("fk_users_pair_user_id_users", type_="foreignkey")
        batch_op.drop_index(batch_op.f("ix_users_pair_user_id"))
        batch_op.drop_column("pair_user_id")
