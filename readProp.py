from jproperties import Properties
import os 
from dotenv import load_dotenv

def readProperties(key):
  load_dotenv()
  return os.getenv(key)
      
