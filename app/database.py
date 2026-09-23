from collections.abc import Generator

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Configuracoes(BaseSettings):
    db_name: str = "livros.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


configuracoes = Configuracoes()

DATABASE_URL = f"sqlite:///./{configuracoes.db_name}"

mecanismo_banco = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
criar_sessao = sessionmaker(bind=mecanismo_banco, autoflush=False, autocommit=False)


class BaseBanco(DeclarativeBase):
    pass


def obter_sessao_banco() -> Generator[Session, None, None]:
    sessao_banco = criar_sessao()
    try:
        yield sessao_banco
    finally:
        sessao_banco.close()