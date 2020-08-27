"""empty message

Revision ID: ca4684cb88b1
Revises: a5c1e2c208d5
Create Date: 2020-08-27 17:33:06.245014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca4684cb88b1'
down_revision = 'a5c1e2c208d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_role')),
    sa.UniqueConstraint('name', name=op.f('uq_role_name'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('public_id', name=op.f('uq_user_public_id'))
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name=op.f('fk_roles_users_role_id_role')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_roles_users_user_id_user'))
    )
    op.drop_table('tbl_users')
    op.drop_table('tbl_roles')
    with op.batch_alter_table('tbl_todos', schema=None) as batch_op:
        batch_op.drop_constraint('fk_tbl_todos_user_id_tbl_users', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_tbl_todos_user_id_user'), 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbl_todos', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_tbl_todos_user_id_user'), type_='foreignkey')
        batch_op.create_foreign_key('fk_tbl_todos_user_id_tbl_users', 'tbl_users', ['user_id'], ['id'])

    op.create_table('tbl_roles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nome', sa.VARCHAR(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_tbl_roles')
    )
    op.create_table('tbl_users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('public_id', sa.VARCHAR(length=50), nullable=True),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('password', sa.VARCHAR(length=80), nullable=True),
    sa.Column('admin', sa.BOOLEAN(), nullable=True),
    sa.CheckConstraint('admin IN (0, 1)', name='ck_tbl_users_admin'),
    sa.PrimaryKeyConstraint('id', name='pk_tbl_users'),
    sa.UniqueConstraint('public_id', name='uq_tbl_users_public_id')
    )
    op.drop_table('roles_users')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
