from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class MembersDataBase(Base):
    __tablename__ = "_members"
    ssn_id = Column("ssn_id", Integer, primary_key=True)
    firstname = Column("_first_name", String)
    username = Column("_user_name", String)
    
    def __init__(self, ssn_id, firstname, username):
        self.ssn_id = ssn_id
        self.firstname = firstname
        self.username = username
    
    def __repr__(self):
        fmt = u'{}({})'
        class_ = self.__class__.__name__
        attrs = sorted(
            (k, getattr(self, k)) for k in self.__mapper__.columns.keys()
        )
        sattrs = u', '.join('{}={!r}'.format(*x) for x in attrs)
        return fmt.format(class_, sattrs)
   


class database:
    def __init__(self):
        self.engine = create_engine("sqlite:///:memory:", echo=True)
        Base.metadata.create_all(bind=self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def push(self, ssn_id, firstname, username):
        member_db = MembersDataBase(ssn_id, firstname, username)
        self.session.add(member_db)
        self.session.commit()

    def print_members(self):
        members = self.session.query(MembersDataBase).all()
        members_text_list ="Members: \n"
        counter = 1
        
        for member in members:
            members_text_list += f"{counter}. {member.firstname}, {member.username}, {member.ssn_id} \n"
        
        return members_text_list
    
    
    def exists(self, ssn_id):
        member = self.session.query(MembersDataBase).filter_by(ssn_id=ssn_id).first()
        return member is not None
    
    
    def create_new_database(self):
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
       
        
    def delete_database(self):
        Base.metadata.drop_all(bind=self.engine)
        
        
    def getid_list(self):
        id_list = []
    
        for member in self.session.query(MembersDataBase):
            id_list.append(member.ssn_id)
        
        return id_list
    
    def remove_user(self, ssn_id):
        member = self.session.query(MembersDataBase).filter_by(ssn_id = ssn_id).first()
        if member:
            self.session.delete(member)
            self.session.commit()

        
    
    
        