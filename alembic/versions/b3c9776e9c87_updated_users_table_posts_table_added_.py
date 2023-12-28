"""updated users table, posts table, added comments table, notifications table

Revision ID: b3c9776e9c87
Revises: 8b1664379f1a
Create Date: 2023-09-12 14:52:43.688271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c9776e9c87'
down_revision = '8b1664379f1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(
                        timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('comments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(
                        timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.add_column('posts', sa.Column(
        'updated_at', sa.TIMESTAMP(timezone=True), nullable=True))
    op.drop_column('posts', 'title')
    op.add_column('users', sa.Column('name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))
    op.add_column('users', sa.Column(
        'updated_at', sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('users', sa.Column('bio', sa.String(), nullable=True))
    op.add_column('users', sa.Column('email_verified',
                  sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('users', sa.Column(
        'cover_image', sa.String(), nullable=True))
    op.add_column('users', sa.Column(
        'profile_image', sa.String(), nullable=True))
    op.add_column('users', sa.Column(
        'has_notification', sa.Boolean(), nullable=True))
    op.create_unique_constraint('uq_username', 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_username', 'users', type_='unique')
    op.drop_column('users', 'has_notification')
    op.drop_column('users', 'profile_image')
    op.drop_column('users', 'cover_image')
    op.drop_column('users', 'email_verified')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'username')
    op.drop_column('users', 'name')
    op.add_column('posts', sa.Column('title', sa.VARCHAR(),
                  autoincrement=False, nullable=False))
    op.drop_column('posts', 'updated_at')
    op.drop_table('comments')
    op.drop_table('notifications')
    # ### end Alembic commands ###