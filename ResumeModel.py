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
        self.__parse_contact()
        
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
    
    def __parse_contact(self) -> list[list[str]]:
        self.__personal_details,self.__email,self.__city,self.__phone ,self.__name = extract_personal_details(self.__doc)
        
    @property
    def personal_details(self) -> list[list]:
        """Get Candidate personal details as required in resume"""
        return self.__personal_details
    
        