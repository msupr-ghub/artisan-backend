"""bootstrap tables

Revision ID: 67ab74fb7e4e
Revises: 
Create Date: 2025-02-01 15:26:40.832873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67ab74fb7e4e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.String, primary_key=True, index=True, nullable=False),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
        sa.Column("is_superuser", sa.Boolean, nullable=False),
    )

    op.create_index("ix_user_username", "user", ["username"], unique=True)
    op.create_index("ix_user_email", "user", ["email"], unique=True)
    op.create_table(
        "chat",
        sa.Column("id", sa.String, primary_key=True, index=True, nullable=False),
    )

    op.create_table(
        "message",
        sa.Column("id", sa.String, primary_key=True, index=True, nullable=False),
        sa.Column("chat_id", sa.String, nullable=False),
        sa.Column("user_id", sa.String, nullable=False),
    )

    op.create_index("ix_message_chat_id", "message", ["chat_id"])
    op.create_index("ix_message_user_id", "message", ["user_id"])
    op.create_foreign_key("fk_message_chat_id", "message", "chat", ["chat_id"], ["id"])
    op.create_foreign_key("fk_message_user_id", "message", "user", ["user_id"], ["id"])



def downgrade() -> None:
    op.drop_table("message")
    op.drop_table("chat")
    op.drop_table("user")
