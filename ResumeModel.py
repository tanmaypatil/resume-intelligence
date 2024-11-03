from typing import List,Sequence
from format_util import *
class ResumeModel:
    def __init__(self,genDoc : object):
        self.__doc = genDoc
        self.__name = ''
        self.__email =''
        self.__title =''
        self.__city =''
        self.__phone = ''
        self.__personal_details = []
        self.__summary =''
        self.__experience_details = []
        self._skills = []
        self.__parse_contact()
        self.__parse()
        
    @property
    def name(self) -> str:
        """Get Candidate name"""
        return self.__name
    
    @property
    def email(self) -> str:
        """Get Candidate email"""
        return self.__email
    
    @property
    def title(self) -> str:
        """Get Candidate job title"""
        return self.__title

    @property
    def city(self) -> str:
        """Get Candidate city of residence"""
        return self.__city

    @property
    def phone(self) -> str:
        """Get Candidate phone details"""
        return self.__phone
    
    @property
    def summary(self) -> str:
        """Get Candidate Summary details"""
        return self.__summary
    
    @property
    def skills(self) -> str:
        """Get Candidate Skills """
        return self.__skills
    
    def __parse_contact(self):
        self.__personal_details,self.__email,self.__city,self.__phone ,self.__name = extract_personal_details(self.__doc)
        # make the name to upper case 
        self.__name.upper()
        
    @property
    def personal_details(self) -> list[list]:
        """Get Candidate personal details as required in resume"""
        return self.__personal_details
    
    def __parse_experience(self,experience):
      for e in experience:
        ach = [ ach.join('\n') for ach in e.achievements ] 
        ()
    
    def __parse(self):
        # parse summary
        self.__summary = self.__doc.get("summary")
        # parse only technical skills 
        sk = self.__doc.get("skills")
        self.__skills = sk['technical']
        experience = self._doc.get("experience")
        self.__parse_experience(experience)
        