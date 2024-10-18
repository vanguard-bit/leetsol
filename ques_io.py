import requests
import re
from question_dict import question


def sherd_html(ques_info):

    regobj = re.compile(r"(<.*?>)", re.DOTALL)
    ques_info = regobj.sub("", ques_info)
    regobj = re.compile(r"(&quot;)", re.DOTALL)
    ques_info = regobj.sub("\"", ques_info)
    regobj = re.compile(r"(&lt;)", re.DOTALL)
    ques_info = regobj.sub("<", ques_info)
    regobj = re.compile(r"(&gt;)", re.DOTALL)
    ques_info = regobj.sub(">", ques_info)
    regobj = re.compile(r"(&le;)", re.DOTALL)
    ques_info = regobj.sub("<=", ques_info)
    regobj = re.compile(r"(&ge;)", re.DOTALL)
    ques_info = regobj.sub(">=", ques_info)
    regobj = re.compile(r"(&nbsp;)", re.DOTALL)
    ques_info = regobj.sub(" ", ques_info)
    regobj = re.compile(r"(&#(\d+);)", re.DOTALL)
    val = regobj.findall(ques_info)
    if val:
        val = int(val[0][1])
        ques_info = regobj.sub(chr(val), ques_info)
    regobj = re.compile(r"(&.*;)", re.DOTALL)
    ques_info = regobj.sub(" ", ques_info)
    return ques_info


def ques_io(QID):
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
        "variables": {"titleSlug": question[QID]["title_slug"]}
    }
    req = requests.post(Base_Url, json=data)
    # print(fr'{req.text!s}')
    image = False
    imgreg = re.compile(r'<img.*?\".*?\"(https.*?)\"', re.DOTALL)
    res = imgreg.findall(req.text)
    if res:
        print()
        print(res)
        print()
        if res:
            image = res

    regobj = re.compile(r'.*?content.*?\".*?\"(.*)\"}}}', re.S)
    mo = regobj.search(req.text)
# print(mo.groups()[0])

    if mo:
        # bsobj = bs4.BeautifulSoup(mo.groups()[0], features="html.parser")

        ques_ = mo.groups()[0]
        ques_info = sherd_html(ques_)

        regio = re.compile(
            r'Input[:\n\\n]*(.*?)\\n.*?Output[:\n\\n]*(.*?)\\n',
            (re.S))

        mo = regio.findall(ques_info)
        # print(mo)
        _ = ["Input", "Output"]
        io_list = []
        for ele in mo:
            i = 0
            for e in ele:
                io_list.append(_[i] if i < 2 else '')
                val = e.split(', ')
                for x in val:
                    io_list.append(x.strip())
                io_list.append('\n')
                i += 1
        # print(io_list)
        regobj = re.compile(r"(\\n)", re.DOTALL)
        ques_info = regobj.sub("\n", ques_info)
        regobj = re.compile(r"(\\t)", re.DOTALL)
        ques_info = regobj.sub("\t", ques_info)
        # print(ques_info)
        return (ques_info, io_list, image)


if __name__ == '__main__':
    for ele in ques_io(1):
        print(ele)
