"""Add due_in column to deadline

Revision ID: bbc121983af8
Revises: 
Create Date: 2024-03-31 17:06:35.632880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbc121983af8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('deadline', schema=None) as batch_op:
        batch_op.add_column(sa.Column('due_in', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('overdue', sa.Boolean(), nullable=True))
        batch_op.drop_column('overdue_by')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('deadline', schema=None) as batch_op:
        batch_op.add_column(sa.Column('overdue_by', sa.VARCHAR(length=50), nullable=True))
        batch_op.drop_column('overdue')
        batch_op.drop_column('due_in')

    # ### end Alembic commands ###
