"""empty message

Revision ID: effd6393dcd8
Revises: 9be3516a9e1f
Create Date: 2018-03-25 19:22:17.948738

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'effd6393dcd8'
down_revision = '9be3516a9e1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('type', sa.String(length=128), nullable=True))
    op.drop_column('course', 'branch')
    op.add_column('result', sa.Column('score', sa.String(length=16), nullable=True))
    op.add_column('result', sa.Column('sub', sa.String(length=8), nullable=True))
    op.drop_column('result', 'sub6')
    op.drop_column('result', 'sub7')
    op.drop_column('result', 'sub4')
    op.drop_column('result', 'sub5')
    op.drop_column('result', 'sub2')
    op.drop_column('result', 'sub3')
    op.drop_column('result', 'sub1')
    op.drop_column('result', 'sub8')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('result', sa.Column('sub8', mysql.VARCHAR(length=8), nullable=True))
    op.add_column('result', sa.Column('sub1', mysql.VARCHAR(length=8), nullable=True))
    op.add_column('result', sa.Column('sub3', mysql.VARCHAR(length=8), nullable=True))
    op.add_column('result', sa.Column('sub2', mysql.VARCHAR(length=8), nullable=True))
    op.add_column('result', sa.Column('sub5', mysql.VARCHAR(length=8), nullable=True))
    op.add_column('result', sa.Column('sub4', mysql.VARCHAR(length=8), nullable=True))
    op.add_column('result', sa.Column('sub7', mysql.VARCHAR(length=8), nullable=True))
    op.add_column('result', sa.Column('sub6', mysql.VARCHAR(length=8), nullable=True))
    op.drop_column('result', 'sub')
    op.drop_column('result', 'score')
    op.add_column('course', sa.Column('branch', mysql.VARCHAR(length=128), nullable=True))
    op.drop_column('course', 'type')
    # ### end Alembic commands ###
