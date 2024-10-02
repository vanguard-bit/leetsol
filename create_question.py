import requests
import bs4
import re
from question_dict import question
import pprint

Base_Url = "https://leetcode.com/graphql/"
data = {
    "query": """

query consolePanelConfig($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    content
    # questionFrontendId
    # questionTitle
    # exampleTestcaseList
  }
}
    """,
    "variables": {"titleSlug": question[1461]["title_slug"]}
}
req = requests.post(Base_Url, json=data)
# print(fr'{req.text!s}')

regobj = re.compile(r'.*?content.*?\".*?\"(.*)\"}}}', re.S)
mo = regobj.search(req.text)
# print(mo.groups()[0])

if mo:
    bsobj = bs4.BeautifulSoup(mo.groups()[0], features="html.parser")
# regi = re.compile(r'(example.*input:(.*?)output.(.*?)Explanation.*?)', (re.S | re.I))
    regio = re.compile(r'Input[:\n\\n]*(.*?)\\n.*?Output[:\n\\n]*(.*?)\\n', (re.S))

    for script in bsobj(["script", "style"]):
        script.extract()
    text = bsobj.get_text()
    lines = (line.strip('\n ') for line in text.splitlines())
    chunks = (phrase.strip() for phrase in lines if phrase)
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # print(text)
    mo = regio.findall(text)
    print(mo)
    _ = ["Input", "Output"]
    print()
    for ele in mo:
        i = 0
        for e in ele:
            print(_[i] if i < 2 else '')
            val = e.split(', ')
            for x in val:
                print(x.strip(), end=" ")
            print()
            i += 1
        print()


