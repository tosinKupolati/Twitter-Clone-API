"""altered_email_verfied_column

Revision ID: b8171228ce86
Revises: 3995a05f1a0e
Create Date: 2023-09-14 12:44:20.497171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8171228ce86'
down_revision = '3995a05f1a0e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("users", "email_verified")
    op.add_column("users", sa.Column("email_verified",
                  sa.Boolean, server_default="False"))


def downgrade() -> None:
    op.drop_column("users", "email_verified")
    op.add_column("users", sa.Column(
        "email_verified", sa.TIMESTAMP(timezone=True)))
