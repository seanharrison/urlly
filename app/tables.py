import sqlalchemy as sa

from app.lib import gen_id

metadata = sa.MetaData()

urls = sa.Table(
    'urls',
    metadata,
    sa.Column('id', sa.String, primary_key=True, default=lambda: gen_id(7)),
    sa.Column('url', sa.String, nullable=False),
)
