"""empty message

Revision ID: 02618058d921
Revises: 242d6aa0caab
Create Date: 2023-05-11 00:27:27.093754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02618058d921'
down_revision = '242d6aa0caab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.drop_constraint('likes_user_id_post_id_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.create_unique_constraint('likes_user_id_post_id_key', ['user_id', 'post_id'])

    # ### end Alembic commands ###