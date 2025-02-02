"""bootstrap tables

Revision ID: 67ab74fb7e4e
Revises: 
Create Date: 2025-02-01 15:26:40.832873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '67ab74fb7e4e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, index=True, nullable=False),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
        sa.Column("is_superuser", sa.Boolean, nullable=False),
        sa.Column("user_type", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), server_default=sa.text("now()"), default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=False), server_default=sa.text("now()"), default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    op.create_index("ix_user_username", "user", ["username"], unique=True)
    op.create_index("ix_user_email", "user", ["email"], unique=True)
    op.create_table(
        "chat",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, index=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), server_default=sa.text("now()"), default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=False), server_default=sa.text("now()"), default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_foreign_key("fk_chat_user_id", "chat", "user", ["user_id"], ["id"])

    op.create_table(
        "message",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, index=True, nullable=False),
        sa.Column("chat_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("content", sa.String, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), server_default=sa.text("now()"), default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=False), server_default=sa.text("now()"), default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column("type", sa.String, nullable=False)
    )

    op.create_index("ix_message_chat_id", "message", ["chat_id"])
    op.create_index("ix_message_user_id", "message", ["user_id"])
    op.create_foreign_key("fk_message_chat_id", "message", "chat", ["chat_id"], ["id"])
    op.create_foreign_key("fk_message_user_id", "message", "user", ["user_id"], ["id"])

    # insert a system user in users table, this user is used to track system messages
    op.execute(
        """
        INSERT INTO "user" (id, username, email, hashed_password, is_active, is_superuser, user_type)
        VALUES ('123e4567-e89b-12d3-a456-426614174001', 'system', 'system@artisan.ai', 'system', true, false, 'SYSTEM')
        """
    )



def downgrade() -> None:
    op.drop_table("message")
    op.drop_table("chat")
    op.drop_table("user")
