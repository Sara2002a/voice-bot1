"""create table voices

Revision ID: 7afcfddb498b
Revises: 9e94a2a827f6
Create Date: 2022-01-12 19:39:10.942976

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from models.voices import create_datetime_trigger, drop_datetime_trigger

revision = "7afcfddb498b"
down_revision = "9e94a2a827f6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "voices",
        sa.Column("uuid", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="Resource UUID"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Resource creation date"),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False, comment="Resource activity status"),
        sa.Column("modified_at", postgresql.TIMESTAMP(timezone=True), nullable=False, comment="Resource modification date"),
        sa.Column("title", sa.VARCHAR(length=255), nullable=False, comment="Title"),
        sa.Column("performer", sa.VARCHAR(length=255), nullable=False, comment="Performer"),
        sa.Column("link", sa.VARCHAR(length=2000), nullable=False, comment="Resource link"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("link"),
        sa.UniqueConstraint("title", "performer", name="voice_constraint"),
        schema="public",
        comment="Voices"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("voices", schema="public")
