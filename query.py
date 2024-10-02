import requests

data = {

    "query": """query questionEditorData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
      solution {
      paidOnly
      hasVideoSolution
      canSeeDetail
    }
      }
    }
    """,
    "variables": {"titleSlug": "two-sum"}
}

Headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}
req = requests.post("https://leetcode.com/graphql", json=data, headers=Headers)
with open("wih.html", "w") as file:
    file.write(req.text)
import pprint
pprint.pprint(req.text)
