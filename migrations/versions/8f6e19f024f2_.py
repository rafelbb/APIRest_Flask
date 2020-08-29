"""empty message

Revision ID: 8f6e19f024f2
Revises: ae6b5dd5674c
Create Date: 2020-08-29 18:54:23.838813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f6e19f024f2'
down_revision = 'ae6b5dd5674c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=50), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_todo_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_todo'))
    )
    op.drop_table('tbl_todos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_todos',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=50), nullable=True),
    sa.Column('complete', sa.BOOLEAN(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.CheckConstraint('complete IN (0, 1)', name='ck_tbl_todos_complete'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_tbl_todos_user_id_user'),
    sa.PrimaryKeyConstraint('id', name='pk_tbl_todos')
    )
    op.drop_table('todo')
    # ### end Alembic commands ###
