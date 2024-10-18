import requests
import re
from question_dict import question


def snip_gen(QID):
    Base_Url = "https://leetcode.com/graphql/"

    data = {
        "query": """query questionEditorData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        codeSnippets {
          lang
          langSlug
          code
        }
      }
    }
    """,
        "variables": {"titleSlug": question[QID]["title_slug"]}
    }

    req = requests.post(Base_Url, json=data)
# print(req.text)

    regobj = re.compile(r'python3.*?code.*?:\"(.*?)\"}', re.DOTALL)
    res = regobj.findall(req.text)
    Paid = False
    if res:
        res = re.sub(r'\\n', '\n', res[0])
        print(res)
    else:
        Paid = True

    return (Paid, res)
