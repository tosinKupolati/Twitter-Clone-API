"""add content column to posts table

Revision ID: bd92bec42609
Revises: d43ec1e80b41
Create Date: 2023-06-30 20:32:26.058557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd92bec42609'
down_revision = 'd43ec1e80b41'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade():
    op.drop_column("posts", "content")
