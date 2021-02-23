"""empty message

Revision ID: 6a009c7d010d
Revises: 
Create Date: 2021-02-22 09:26:08.245507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a009c7d010d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('regions',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('parent_slug', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['parent_slug'], ['regions.slug'], ),
    sa.PrimaryKeyConstraint('slug')
    )
    op.create_table('ports',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('code', sa.String(length=5), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('parent_slug', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['parent_slug'], ['regions.slug'], ),
    sa.PrimaryKeyConstraint('code'),
    sa.UniqueConstraint('code')
    )
    op.create_table('prices',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('orig_code', sa.String(), nullable=False),
    sa.Column('dest_code', sa.String(), nullable=False),
    sa.Column('day', sa.DATE(), nullable=True),
    sa.Column('price', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['dest_code'], ['ports.code'], ),
    sa.ForeignKeyConstraint(['orig_code'], ['ports.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prices')
    op.drop_table('ports')
    op.drop_table('regions')
    # ### end Alembic commands ###
