"""added conversation and message tables

Revision ID: 4619fd898c57
Revises: 1223b6269b92
Create Date: 2023-05-14 07:17:08.914539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4619fd898c57'
down_revision = '1223b6269b92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_one_id', sa.Integer(), nullable=True),
    sa.Column('user_two_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_one_id'], ['users.id'], name=op.f('fk_conversations_user_one_id_users')),
    sa.ForeignKeyConstraint(['user_two_id'], ['users.id'], name=op.f('fk_conversations_user_two_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conversation_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name=op.f('fk_messages_conversation_id_conversations')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_messages_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('conversations')
    # ### end Alembic commands ###
