from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    queries = relationship("UserQuery", back_populates="user", cascade="all, delete-orphan")
    sources = relationship("UserSource", back_populates="user", cascade="all, delete-orphan")
    topics = relationship("UserTopic", back_populates="user", cascade="all, delete-orphan")

class UserQuery(Base):
    __tablename__ = 'user_queries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    query_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="queries")

class UserSource(Base):
    __tablename__ = 'user_sources'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    source_domain = Column(String(100), nullable=False)  # e.g., 'cnn.com', 'bbc.com'
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="sources")
    
    # Ensure unique combination of user and source
    __table_args__ = (UniqueConstraint('user_id', 'source_domain', name='uq_user_source'),)

class UserTopic(Base):
    __tablename__ = 'user_topics'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    topic_name = Column(String(100), nullable=False)  # e.g., 'AI', 'Technology', 'Politics'
    category = Column(String(50), nullable=False)  # e.g., 'tech', 'sci', 'pol'
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="topics")
    
    # Ensure unique combination of user and topic
    __table_args__ = (UniqueConstraint('user_id', 'topic_name', name='uq_user_topic'),)

# Database setup
def create_database():
    engine = create_engine('sqlite:///news_bot.db')
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = create_engine('sqlite:///news_bot.db')
    Session = sessionmaker(bind=engine)
    return Session() 