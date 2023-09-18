"""Update Archive's Model

Revision ID: 4d766c1cc6a3
Revises: 8da678641556
Create Date: 2023-09-08 09:37:12.109887

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4d766c1cc6a3"
down_revision = "8da678641556"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("archive", "filesize", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column(
        "archive", "requested_on", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "archive", "download_url", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "archive", "collection_json_path", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "archive", "zimfarm_task_id", existing_type=sa.UUID(), nullable=True
    )
    op.drop_column("archive", "filename")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "archive",
        sa.Column("filename", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.alter_column(
        "archive", "zimfarm_task_id", existing_type=sa.UUID(), nullable=False
    )
    op.alter_column(
        "archive", "collection_json_path", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "archive", "download_url", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "archive", "requested_on", existing_type=postgresql.TIMESTAMP(), nullable=False
    )
    op.alter_column("archive", "filesize", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###
