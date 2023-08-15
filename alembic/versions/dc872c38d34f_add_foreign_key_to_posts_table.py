"""add foreign key to posts table

Revision ID: dc872c38d34f
Revises: 3eb8694cc7a0
Create Date: 2023-07-02 20:05:29.560379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc872c38d34f'
down_revision = '3eb8694cc7a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_user_id_fkey", source_table="posts", referent_table="users", local_cols=[
                          "user_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_user_id_fkey", table_name="posts")
    op.drop_column("posts", "user_id")
