"""create table user voice relations

Revision ID: 7c60ed9fe75c
Revises: 751a1c4e308e
Create Date: 2022-03-09 15:44:13.570538

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from models.user_voice_relation import create_datetime_trigger, drop_datetime_trigger

revision = "7c60ed9fe75c"
down_revision = "751a1c4e308e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        # fmt: off
        "user_voice_relations",
        sa.Column("uuid", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False, comment="Resource UUID"),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Resource creation date"),
        sa.Column("modified_at", postgresql.TIMESTAMP(timezone=True), nullable=False, comment="Resource modification date"),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False, comment="Resource activity status"),
        sa.Column("user_uuid", postgresql.UUID(), nullable=False, comment="User UUID"),
        sa.Column("voice_uuid", postgresql.UUID(), nullable=False, comment="Voice UUID"),
        sa.ForeignKeyConstraint(["user_uuid"], ["public.users.uuid"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["voice_uuid"], ["public.voices.uuid"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("user_uuid", "voice_uuid", name="user_voice_constraint"),
        schema="public",
        comment="User voice relations"
    )
    create_datetime_trigger(target=None, bind=op.get_bind())


def downgrade():
    drop_datetime_trigger(target=None, bind=op.get_bind())
    op.drop_table("user_voice_relations", schema="public")
