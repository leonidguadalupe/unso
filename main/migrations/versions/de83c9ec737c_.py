"""empty message

Revision ID: de83c9ec737c
Revises: 6a009c7d010d
Create Date: 2021-02-23 06:56:27.728802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de83c9ec737c'
down_revision = '6a009c7d010d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'ports', ['code'])
    op.create_index('price_index', 'prices', ['orig_code', 'dest_code', 'day'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('price_index', table_name='prices')
    op.drop_constraint(None, 'ports', type_='unique')
    # ### end Alembic commands ###
