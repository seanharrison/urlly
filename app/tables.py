import sqlalchemy as sa

from app import settings
from app.lib import gen_id

metadata = sa.MetaData()

urls = sa.Table(
    'urls',
    metadata,
    sa.Column(
        'id', sa.String, primary_key=True, default=lambda: gen_id(settings.GEN_ID_BYTES)
    ),
    sa.Column('target', sa.String, nullable=False),
)
