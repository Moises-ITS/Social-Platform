from sqlalchemy import (
    text,
    create_engine,
    select,
    ForeignKey,
    Named,
    TypedColumns,
    Table,
    Column,
    Integer,
    String,
    MetaData,
)
from sqlalchemy.orm import sessionmaker
from app.config import settings

#compose.yaml -> "POSTGRES_USER:PASTGRES_PASSWORD@localhost:5432/POSTGRES_DB"
DATABASE_URL = (
    "postgresql+psycopg://"
    "social:devpassword@localhost:5432/socialdb"
)

metadata_obj = MetaData()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

class user_cols(TypedColumns):
    id: Named[int] = Column(primary_key=True)
    name: Named[str | None] = Column(String(30))
    fullname: Named[str | None]

typed_user_table = Table("user_account", metadata_obj, user_cols)

class address_columns(TypedColumns):
    id: Named[int] = Column(primary_key=True)
    user_id: Named[int] = Column(ForeignKey("user_account.id"))
    email_address: Named[str]
    __row_pos__: tuple[int, int, str]

typed_address_table = Table("address", metadata_obj, address_columns)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    echo=False,
)
def check_database_connection() -> bool:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return result.scalar_one() == 1

"""
with Session.begin() as session:
    #Query for User objects
    statement = select(User).filter_by(name="ed")
    #list of User objects
    user_obj = session.scalars(statement).all()
    #Query for individual columns
    statement = select(User.name, User.fullname)
    #List of Row objects
    rows = session.execute(statement).all()
    user1 = User(name="user1")
    session.add(user1)
    #to add a list of users
    session.add_all([user1, user2, user3])
    #to delete
    session.delete(obj1)
"""