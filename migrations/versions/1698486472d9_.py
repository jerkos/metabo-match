"""empty message

Revision ID: 1698486472d9
Revises: 1eca56e2d2b3
Create Date: 2015-06-24 14:51:16.498000

"""

# revision identifiers, used by Alembic.
revision = '1698486472d9'
down_revision = '1eca56e2d2b3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=500), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), nullable=True),
                    sa.Column('content', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.add_column(u'softwares', sa.Column('last_position_by_global_rate', sa.Integer(), nullable=True))
    op.add_column(u'softwares', sa.Column('last_position_by_perf_upvotes', sa.Integer(), nullable=True))
    op.add_column(u'softwares', sa.Column('last_position_by_support_upvotes', sa.Integer(), nullable=True))
    op.add_column(u'softwares', sa.Column('last_position_by_tot_upvotes', sa.Integer(), nullable=True))
    op.add_column(u'softwares', sa.Column('last_position_by_ui_upvotes', sa.Integer(), nullable=True))
    op.add_column(u'softwares', sa.Column('last_position_by_users_rates', sa.Integer(), nullable=True))
    op.add_column(u'softwares', sa.Column('nb_winner_of_the_day_rate', sa.Integer(), nullable=True))
    op.add_column(u'softwares', sa.Column('nb_winner_of_the_day_upvote', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'softwares', 'nb_winner_of_the_day_upvote')
    op.drop_column(u'softwares', 'nb_winner_of_the_day_rate')
    op.drop_column(u'softwares', 'last_position_by_users_rates')
    op.drop_column(u'softwares', 'last_position_by_ui_upvotes')
    op.drop_column(u'softwares', 'last_position_by_tot_upvotes')
    op.drop_column(u'softwares', 'last_position_by_support_upvotes')
    op.drop_column(u'softwares', 'last_position_by_perf_upvotes')
    op.drop_column(u'softwares', 'last_position_by_global_rate')
    op.drop_table('articles')
    ### end Alembic commands ###
