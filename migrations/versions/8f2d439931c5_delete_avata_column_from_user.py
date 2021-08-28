"""delete avata column from user

Revision ID: 8f2d439931c5
Revises: 3b8b51eb2e59
Create Date: 2021-08-20 15:37:09.622730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f2d439931c5'
down_revision = '3b8b51eb2e59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('avatar')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.BLOB(), nullable=True))

    # ### end Alembic commands ###
