"""timestamp_col_names

Revision ID: 9c40d4d8f361
Revises: 4adfa1500488
Create Date: 2020-12-09 23:22:36.286246

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '9c40d4d8f361'
down_revision = '4adfa1500488'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('urls', 'timestamp', new_column_name='created')
    op.alter_column('urls_log', 'timestamp', new_column_name='logged')


def downgrade():
    op.alter_column('urls', 'created', new_column_name='timestamp')
    op.alter_column('urls_log', 'logged', new_column_name='timestamp')
