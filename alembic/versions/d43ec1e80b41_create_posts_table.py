"""create posts table

Revision ID: d43ec1e80b41
Revises: 
Create Date: 2023-06-30 14:17:27.298922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd43ec1e80b41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer, primary_key=True,
                    nullable=False), sa.Column("title", sa.String, nullable=False))


def downgrade():
    op.drop_table("posts")
