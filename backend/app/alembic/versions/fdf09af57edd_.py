"""empty message

Revision ID: fdf09af57edd
Revises: 30a532f1b3fa
Create Date: 2024-07-01 06:37:39.351701

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from tidb_vector.sqlalchemy import VectorType


# revision identifiers, used by Alembic.
revision = "fdf09af57edd"
down_revision = "30a532f1b3fa"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("chunks", sa.Column("relations", sa.JSON(), nullable=True))
    op.add_column(
        "chunks",
        sa.Column(
            "source_uri", sqlmodel.sql.sqltypes.AutoString(length=512), nullable=True
        ),
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("chunks", "relations")
    op.drop_column("chunks", "source_uri")
    # ### end Alembic commands ###
