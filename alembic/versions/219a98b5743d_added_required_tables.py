"""Added required tables

Revision ID: 219a98b5743d
Revises: 
Create Date: 2021-07-12 02:59:50.503160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '219a98b5743d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('follows',
    sa.Column('follows_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('following_id', sa.Integer(), nullable=False),
    sa.CheckConstraint('user_id != following_id', name='user_is_not_author'),
    sa.ForeignKeyConstraint(['following_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follows_id'),
    sa.UniqueConstraint('user_id', 'following_id', name='unique_follow')
    )
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('User', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['User'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_title'), 'groups', ['title'], unique=True)
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('User', sa.Integer(), nullable=False),
    sa.Column('Group', sa.Integer(), nullable=True),
    sa.Column('pub_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['Group'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['User'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_text'), 'posts', ['text'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('User', sa.Integer(), nullable=True),
    sa.Column('Post', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['Post'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['User'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_text'), 'comments', ['text'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_text'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_posts_text'), table_name='posts')
    op.drop_table('posts')
    op.drop_index(op.f('ix_groups_title'), table_name='groups')
    op.drop_table('groups')
    op.drop_table('follows')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
