"""empty message

Revision ID: 77de0b812953
Revises: 40878da91325
Create Date: 2017-03-08 20:42:13.371186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77de0b812953'
down_revision = '40878da91325'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flicks_list_item', sa.Column('ordering', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flicks_list_item', 'ordering')
    # ### end Alembic commands ###
