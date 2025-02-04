from sqlalchemy import Column, Integer, String, DateTime

from ..database import Base

class Article(Base):
    __tablename__ = 'articles'

    article_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    title = Column(String, nullable=True)
    author = Column(String)
    content = Column(String, nullable=False)
    published_at = Column(DateTime)

    def __repr__(self):
        return "<Article(article_id='%s', author='%s', url='%s')>" % (self.article_id, self.author, self.url)
