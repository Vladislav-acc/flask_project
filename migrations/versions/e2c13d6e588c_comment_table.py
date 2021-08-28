"""comment table

Revision ID: e2c13d6e588c
Revises: 7268da1293e7
Create Date: 2021-08-13 16:40:20.345116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2c13d6e588c'
down_revision = '7268da1293e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(length=400), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('author', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(length=200), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('author', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('post')
    # ### end Alembic commands ###