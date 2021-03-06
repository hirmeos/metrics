"""empty message

Revision ID: 8b5f58e10869
Revises: 
Create Date: 2019-02-15 18:50:48.558590

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8b5f58e10869'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('scrape',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('uri',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('raw', sa.String(), nullable=False),
    sa.Column('last_checked', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('raw')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('institution', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('approved', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('error',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri_id', sa.Integer(), nullable=False),
    sa.Column('scrape_id', sa.Integer(), nullable=False),
    sa.Column('origin', sa.Integer(), nullable=False),
    sa.Column('provider', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('last_successful_scrape_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['scrape_id'], ['scrape.id'], ),
    sa.ForeignKeyConstraint(['uri_id'], ['uri.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.String(), nullable=False),
    sa.Column('origin', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['uri_id'], ['uri.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uri_id', 'subject_id')
    )
    op.create_table('metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri_id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.HSTORE(text_type=sa.Text()), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['uri_id'], ['uri.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.create_table('uris_users',
    sa.Column('uri_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['uri_id'], ['uri.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('uri_id', 'user_id')
    )
    op.create_table('url',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('uri_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['uri_id'], ['uri.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('raw_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('scrape_id', sa.Integer(), nullable=False),
    sa.Column('external_id', sa.String(), nullable=True),
    sa.Column('origin', sa.Integer(), nullable=False),
    sa.Column('provider', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('reason_for_deletion', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['scrape_id'], ['scrape.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('external_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('raw_event')
    op.drop_table('url')
    op.drop_table('uris_users')
    op.drop_table('roles_users')
    op.drop_table('metric')
    op.drop_table('event')
    op.drop_table('error')
    op.drop_table('user')
    op.drop_table('uri')
    op.drop_table('scrape')
    op.drop_table('role')
    # ### end Alembic commands ###
