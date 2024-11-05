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
        self.__education_details = []
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
    
    @property
    def experience_details(self) -> list[tuple]:
        """Get Candidate experience details as required in resume"""
        return self.__experience_details
    
    @property
    def education_details(self) -> list[tuple]:
        """Get Candidate education details as required in resume"""
        return self.__education_details
    
    def __parse_experience(self,exp_arr):
      for e in exp_arr:
        company = e['company']
        position = e['position']
        duration = e['duration']
        ach_list =  e['achievements']
        print(f"type of ach_list {type(ach_list)}")
        ach_str =  ("\n").join(ach_list) 
        exp_obj = (company,position,duration,ach_str)
        self.__experience_details.append(exp_obj)

    def __parse_education(self,edu_arr):
      for e in edu_arr:
        institutionName = e['institutionName']
        degreeName = e['degreeName']
        duration = e['duration']
        edu_obj = (institutionName,degreeName,duration)
        self.__education_details.append(edu_obj)
    
    def __parse(self):
        # parse summary
        self.__summary = self.__doc.get("summary")
        # parse only technical skills 
        sk = self.__doc.get("skills")
        self.__skills = sk['technical']
        experience = self.__doc.get("experience")
        self.__parse_experience(experience)
        education = self.__doc.get("education")
        self.__parse_education(education)
        