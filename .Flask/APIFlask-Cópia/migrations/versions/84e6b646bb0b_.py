"""empty message

Revision ID: 84e6b646bb0b
Revises: c0e1647419d8
Create Date: 2024-06-29 07:39:26.126437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84e6b646bb0b'
down_revision = 'c0e1647419d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('formacao',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('descricao', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('formacao')
    # ### end Alembic commands ###
