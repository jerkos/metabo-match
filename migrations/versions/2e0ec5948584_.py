"""empty message

Revision ID: 2e0ec5948584
Revises: None
Create Date: 2015-06-01 10:09:17.347000

"""

# revision identifiers, used by Alembic.
revision = '2e0ec5948584'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('upvotes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('sentence_software_mapping_id', sa.Integer(), nullable=False),
                    sa.Column('date_created', sa.Date(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('upvotes')
    ### end Alembic commands ###
