"""empty message

Revision ID: 3c685d7687ca
Revises: 079c346338b6
Create Date: 2019-06-16 15:56:03.229528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c685d7687ca'
down_revision = '079c346338b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('index_moviename', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'index_moviename')
    # ### end Alembic commands ###
