"""empty message

Revision ID: 29edd350b3da
Revises: None
Create Date: 2014-11-17 17:43:16.967000

"""

# revision identifiers, used by Alembic.
revision = '29edd350b3da'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('softwares',
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('programming_language', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('tags',
    sa.Column('tag', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('tag')
    )
    op.create_table('tags_software_mapping',
    sa.Column('software_name', sa.String(), nullable=False),
    sa.Column('tag_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['software_name'], ['softwares.name'], ),
    sa.ForeignKeyConstraint(['tag_name'], ['tags.tag'], )
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('software_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['software_id'], ['softwares.name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('tags_software_mapping')
    op.drop_table('tags')
    op.drop_table('softwares')
    ### end Alembic commands ###
