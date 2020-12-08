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
    sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
)

urls_log = sa.Table(
    'urls_log',
    metadata,
    sa.Column('url_id', sa.ForeignKey('urls.id'), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
)
