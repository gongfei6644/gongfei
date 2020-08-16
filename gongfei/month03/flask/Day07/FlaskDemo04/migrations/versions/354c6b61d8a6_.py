"""empty message

Revision ID: 354c6b61d8a6
Revises: 097b49841805
Create Date: 2019-05-30 14:28:01.050157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '354c6b61d8a6'
down_revision = '097b49841805'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wife', sa.Column('teacher_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'wife', ['teacher_id'])
    op.create_foreign_key(None, 'wife', 'teacher', ['teacher_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wife', type_='foreignkey')
    op.drop_constraint(None, 'wife', type_='unique')
    op.drop_column('wife', 'teacher_id')
    # ### end Alembic commands ###
