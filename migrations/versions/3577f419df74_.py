"""empty message

Revision ID: 3577f419df74
Revises: None
Create Date: 2015-05-24 12:13:15.605000

"""

# revision identifiers, used by Alembic.
revision = '3577f419df74'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('scripts', 'software_id',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('scripts', 'software_id',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    ### end Alembic commands ###