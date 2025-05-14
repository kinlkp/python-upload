from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Index

Base = declarative_base()

class Host(Base):
    __tablename__ = 'host'
    __tableargs__ = (
        Index('host_hostname_idx', 'hostname')
    )
    id = Column(Integer(), auto_increment=True, primary_key=True)
    hostname = Column(String(), unique=True, nullable=False)
    cpu_threshold = relationship('CPUThreshold', backref='host', lazy='dynamic')
    mem_threshold = relationship('MEMThreshold', backref='host', lazy='dynamic')
    
class CPUThreshold(Base):
    __tablename__ = 'cputhreshold'
    id = Column(Integer(), auto_increment=True, primary_key=True)
    cpu_threshold = Column(Integer(), nullable=False)
    host_id = Column(Integer(), ForeignKey('host.id'), nullable=False)


class MEMThreshold(Base):
    __tablename__ = 'memthreshold'
    id = Column(Integer(), auto_increment=True, primary_key=True)
    mem_threshold = Column(Integer(), nullable=False)
    host_id = Column(Integer(), ForeignKey('host.id'), nullable=False)

