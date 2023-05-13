"""adding notification table


Revision ID: eb4ae4f3b10b
Revises: 9ddf654066ee
Create Date: 2023-05-12 19:46:34.725172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb4ae4f3b10b'
down_revision = '9ddf654066ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('receiving_user_id', sa.Integer(), nullable=True),
    sa.Column('action_user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.String(), nullable=True),
    sa.Column('seen', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['action_user_id'], ['users.id'], name=op.f('fk_notifications_action_user_id_users')),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_notifications_post_id_posts')),
    sa.ForeignKeyConstraint(['receiving_user_id'], ['users.id'], name=op.f('fk_notifications_receiving_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    # ### end Alembic commands ###
