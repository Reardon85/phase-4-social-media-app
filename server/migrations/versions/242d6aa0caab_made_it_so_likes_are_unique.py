"""made it so likes are unique

Revision ID: 242d6aa0caab
Revises: 785c3c3a1b08
Create Date: 2023-05-10 23:15:15.463499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '242d6aa0caab'
down_revision = '785c3c3a1b08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.create_unique_constraint(None, ['user_id', 'post_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('id')

    # ### end Alembic commands ###
