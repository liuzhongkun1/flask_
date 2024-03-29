"""empty message

Revision ID: 8b549d2ad145
Revises: c26358e6bf5e
Create Date: 2022-09-17 07:59:59.574799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b549d2ad145'
down_revision = 'c26358e6bf5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'groupAuth', 'group', ['groupId'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'groupAuth', type_='foreignkey')
    # ### end Alembic commands ###
