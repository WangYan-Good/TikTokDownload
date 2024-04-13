import os
import sys
from urllib.parse import unquote
import re

# config file path
CONFIG_FILE = "Conf/conf.ini"

# section
SECTION_REGULAR = "\[(.*?)\]"
URL_REQULAR = "https?://\S+"

class Conf ():

  def __init__(self) -> None:
    self.section = list()
    self.url_list = list(list())

  def configParser (self, file:str):
    SiftedContext = object()
    SectionName = str()
    SectionFound = False
    Url = object()
    UrlList = list()

    # open the file
    try:
      context =  open (file, "r")
    except Exception as e:
      print ("Read {f} failed {E}".format(f=file, E=e))
    
    # loop config file
    for line in context.readlines(): 

      # match section
      SiftedContext = re.match(SECTION_REGULAR, line)
      if SiftedContext is not None:

        # append url list into self
        if SectionName is not None and SectionFound is True:
          self.url_list.append(UrlList.copy())
          UrlList.clear()

        # receive section 
        SectionName = SiftedContext.groups()[0]
        SectionFound = True

        # add section name into list and make sure the name is unque
        if self.section.count(SectionName) == 0:
          self.section.append(SectionName)
        continue
      
      # match url
      Url = re.match(URL_REQULAR, line)
      if Url is not None:
        
        # append url into url_list
        UrlList.append(Url[0])
        continue
      # print("{section_name}:{section_list}".format(section_name=SectionName, section_list=UrlList))
    self.url_list.append(UrlList.copy())
  
  def getConfigList(self, SectionName:str):
    # defination
    SectionIndex = int()
    
    SectionIndex = self.section.index(SectionName)
    if SectionIndex is not None:
      return self.url_list[SectionIndex]
    else:
      return None

if __name__ == "__main__":
  config = Conf()
  config.configParser(CONFIG_FILE)
  post_list = config.getConfigList("post")
  print(post_list)