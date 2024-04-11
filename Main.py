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
    self.url_list = list()

  def configParser (self, file:str):
    SiftedContext = object()
    SectionIndex = int()
    Url = str()

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
        SectionName = SiftedContext.groups()[0]

        # add section name into list and make sure the name is unque
        if self.section.count(SiftedContext.groups()[0]) == 0:
          self.section.append(SiftedContext.groups()[0])
          self.url_list.append(list())
        continue
      
      # match url
      Url = re.match(URL_REQULAR, line)
      if Url is not None:
        SectionIndex = self.section.index(SectionName)

        # append url into self section list
        if len(self.url_list) < SectionIndex:
          print("url list len: {url_list_len} section[{section_name}] index: {section_index}".format(url_list_len=len(self.url_list), section_name=SectionName, section_index=SectionIndex))
          continue

        if len(self.url_list[SectionIndex]) == 0:
          list(self.url_list[SectionIndex]).append(str())

        if list(self.url_list[SectionIndex]).count(Url.groups()[0]) == 0:
          list(self.url_list[SectionIndex]).append(Url.groups()[0])
          continue

    print(self.self.url_list)
  
  def getPostList(self):
    pass

  def getLiveList():
    pass

if __name__ == "__main__":
  config = Conf()
  config.configParser(CONFIG_FILE)
  # print(config[""])