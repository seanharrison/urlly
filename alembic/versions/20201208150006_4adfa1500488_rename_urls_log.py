"""rename_urls_log

Revision ID: 4adfa1500488
Revises: 3157c9bdc903
Create Date: 2020-12-08 15:00:06.986893

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '4adfa1500488'
down_revision = '3157c9bdc903'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('urls_access_log', 'urls_log')


def downgrade():
    op.rename_table('urls_log', 'urls_access_log')
