"""Create the initial Darukaa.Earth schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-09-19
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '0001_initial_schema'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)

    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('country', sa.String(length=120), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False),
        sa.Column('budget', sa.Float(), nullable=False),
        sa.Column('description', sa.String(length=2000), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_projects_id', 'projects', ['id'], unique=False)

    op.create_table(
        'sites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('note', sa.String(length=1000), nullable=True),
        sa.Column('geometry', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_sites_id', 'sites', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_sites_id', table_name='sites')
    op.drop_table('sites')
    op.drop_index('ix_projects_id', table_name='projects')
    op.drop_table('projects')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
