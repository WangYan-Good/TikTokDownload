import re

# config file path
CONFIG_FILE = "config/douyin/conf.ini"

# section
SECTION_REGULAR = "\[(.*?)\]"
URL_REQULAR = "https?://\S+"

class UrlListConfig ():

  def __init__(self, file:str=CONFIG_FILE) -> None:
    self.section = list()
    self.__url_list = list(list())
    self._configParser(file)

  def _configParser (self, file:str=CONFIG_FILE):
    SiftedContext = object()
    SectionName = str()
    SectionFound = False
    Url = object()
    UrlList = list()

    # open the file
    try:
      context =  open (file, "r")
    
      # loop config file
      for line in context.readlines(): 

        # match section
        SiftedContext = re.match(SECTION_REGULAR, line)
        if SiftedContext is not None:

          # append url list into self
          if SectionName is not None and SectionFound is True:
            self.__url_list.append(UrlList.copy())
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
      self.__url_list.append(UrlList.copy())
      context.close()

    except Exception as e:
      print (e)
  
  def getConfigList(self, SectionName:str):
    if SectionName is None:
      print("Invalide section name {}".format(SectionName))
      return None
    # defination
    SectionIndex = int()
    
    SectionIndex = self.section.index(SectionName)
    if SectionIndex is not None:
      return self.__url_list[SectionIndex]
    else:
      return None
    
  def dump_url_list(self):
    print("Url share link:")
    for sec in self.__url_list:
      print("\t{}".format(sec))