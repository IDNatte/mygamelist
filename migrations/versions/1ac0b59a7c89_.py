"""empty message

Revision ID: 1ac0b59a7c89
Revises: 26561c5f9ad7
Create Date: 2021-09-21 21:51:14.040363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ac0b59a7c89'
down_revision = '26561c5f9ad7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Game', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Game', type_='unique')
    # ### end Alembic commands ###
