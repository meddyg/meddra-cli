from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
from config import DatabaseConfig
from exceptions import DatabaseConnectionError

class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._engine = None
        self._session_factory = None
        
    @property
    def engine(self):
        """Lazy initialization of database engine."""
        if self._engine is None:
            try:
                self._engine = create_engine(self.config.url)
            except Exception as e:
                raise DatabaseConnectionError(self.config.url, e)
        return self._engine
    
    @property
    def session_factory(self):
        """Lazy initialization of session factory."""
        if self._session_factory is None:
            self._session_factory = sessionmaker(bind=self.engine)
        return self._session_factory
    
    def create_session(self) -> Session:
        """Creates a new database session."""
        return self.session_factory()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """Provides a transactional scope around a series of operations."""
        session = self.create_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        """Tests if database connection is working."""
        try:
            with self.session_scope() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(e)
            return False
    
    def close(self) -> None:
        """Closes the database engine."""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None
