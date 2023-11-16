from datetime import date
from requests import get
from xml.etree import ElementTree
import config

datetuple = date.today().timetuple()


# for i in currentdatetime:
#     print(i)

finland = "10YFI-1--------U"
start = ""
end = ""

apiurl = "https://web-api.tp.entsoe.eu/api"
apiurl += "?securityToken=" + config.entsoe
apiurl += "&documentType=A44"
apiurl += "&out_Domain=" + finland
apiurl += "&in_Domain=" + finland
apiurl += "&periodStart=" + str(datetuple[0]) + str(datetuple[1]) + str(datetuple[2]) + "0000"
apiurl += "&periodEnd=" + str(datetuple[0]) + str(datetuple[1]) + str(datetuple[2] + 1) + "2300"

response = get(apiurl)
xmltree = ElementTree.fromstring(response.content)
# apiheaders = ""

# print("Next Day:", datetuple[2] + 1)
print("\nApi Url:", apiurl)
print("-" * 80)
print("Response:\n",response)
print("\nXml-Tree:\n", xmltree)

