"""added user password has and other attributes. added __table_name__

Revision ID: 7b1e440b794a
Revises: 0c501b3c1cad
Create Date: 2023-05-08 19:06:58.196960

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7b1e440b794a'
down_revision = '0c501b3c1cad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=True),
    sa.Column('avatar_url', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_posts_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_comments_post_id_posts')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_comments_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_likes_post_id_posts')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_likes_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )

    op.drop_table('like')
    op.drop_table('comment')
    op.drop_table('post')

    with op.batch_alter_table('followers', schema=None) as batch_op:
        batch_op.drop_constraint('followers_follower_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('followers_followed_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_followers_followed_id_users'), 'users', ['followed_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_followers_follower_id_users'), 'users', ['follower_id'], ['id'])
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('followers', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_followers_follower_id_users'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_followers_followed_id_users'), type_='foreignkey')
        batch_op.create_foreign_key('followers_followed_id_fkey', 'user', ['followed_id'], ['id'])
        batch_op.create_foreign_key('followers_follower_id_fkey', 'user', ['follower_id'], ['id'])

    op.create_table('post',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('post_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('date_posted', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='post_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='post_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('comment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('date_posted', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name='comment_post_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='comment_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='comment_pkey')
    )
    op.create_table('like',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name='like_post_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='like_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='like_pkey')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('likes')
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###
