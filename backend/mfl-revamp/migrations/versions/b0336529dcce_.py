"""empty message

Revision ID: b0336529dcce
Revises: 0a11c2b9cf5c
Create Date: 2017-03-08 18:29:36.972125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0336529dcce'
down_revision = '0a11c2b9cf5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movie', 'avg_rating')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('avg_rating', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
