"""First revision

Revision ID: 774f52cdfeac
Revises:
Create Date: 2023-06-08 23:35:43.347022

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = "774f52cdfeac"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id", sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_on", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_name"), "users", ["name"], unique=True)
    op.create_table(
        "collections",
        sa.Column(
            "id", sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False
        ),
        sa.Column(
            "user_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "email", sqlalchemy_utils.types.email.EmailType(length=255), nullable=False
        ),
        sa.Column("created_on", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expire_on", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_collections_id"), "collections", ["id"], unique=False)
    op.create_table(
        "archives",
        sa.Column(
            "id", sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False
        ),
        sa.Column(
            "collection_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            nullable=False,
        ),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("created_on", sa.DateTime(timezone=True), nullable=False),
        sa.Column("requested_on", sa.DateTime(timezone=True), nullable=False),
        sa.Column("download_url", sa.String(), nullable=False),
        sa.Column("collection_json_path", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("zimfarm_task_id", sa.String(), nullable=False),
        sa.Column("config", sqlalchemy_utils.types.json.JSONType(), nullable=False),
        sa.ForeignKeyConstraint(
            ["collection_id"],
            ["collections.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_archives_id"), "archives", ["id"], unique=False)
    op.create_table(
        "files",
        sa.Column(
            "id", sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False
        ),
        sa.Column(
            "collection_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            nullable=False,
        ),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("authors", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("hash", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["collection_id"],
            ["collections.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_files_id"), "files", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_files_id"), table_name="files")
    op.drop_table("files")
    op.drop_index(op.f("ix_archives_id"), table_name="archives")
    op.drop_table("archives")
    op.drop_index(op.f("ix_collections_id"), table_name="collections")
    op.drop_table("collections")
    op.drop_index(op.f("ix_users_name"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
