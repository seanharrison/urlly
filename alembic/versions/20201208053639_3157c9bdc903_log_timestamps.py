"""log_timestamps

Revision ID: 3157c9bdc903
Revises: bdccd8b5a24a
Create Date: 2020-12-08 05:36:39.916907

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '3157c9bdc903'
down_revision = 'bdccd8b5a24a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'urls_access_log',
        sa.Column('url_id', sa.String(), nullable=False),
        sa.Column(
            'timestamp',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ['url_id'],
            ['urls.id'],
        ),
    )
    op.add_column(
        'urls',
        sa.Column(
            'timestamp',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('urls', 'timestamp')
    op.drop_table('urls_access_log')
    # ### end Alembic commands ###
