import shelve
import re
import predict
import this_month_tags
import pprint
from question_dict import question
import os
import requests
from datetime import date


def get_file():
    name = ''
    val = os.listdir(".\\results")
    val.sort(key=lambda x: int(x[4: -4]))
    if val:
        name = 'results\\res_%d.txt' % (int(val[-1][4:-4]) + 1)
        return name
    return "results\\res_1.txt"


def asked_ques():
    today_obj = date.today()
    this_month = int(today_obj.month)
    this_year = int(today_obj.year)
    data = {

        "query": """query dailyCodingQuestionRecords($year: Int!, $month: Int!) {
      dailyCodingChallengeV2(year: $year, month: $month) {
        challenges {
          date
          question {
            questionFrontendId
            title
          }
        }
        weeklyChallenges {
          date
          question {
            questionFrontendId
            title
          }
        }
      }
    }""",
        "variables": f"""{{"year": {this_year}, "month": {this_month} }}"""
    }

    req = requests.post("https://leetcode.com/graphql", json=data)

    regobj = re.compile(r"\{\"date\".*?(\d+-\d+-\d+).*?\"questionFrontendId\".*?(\d+).*?}},")
    asked_date = {}
    for dat, fqid in regobj.findall(req.text):
        asked_date[int(fqid)] = dat

    return asked_date


def comp(shelve_name, asked):
    # if __name__ == '__main__':
    name_list = []
    shelveFile = shelve.open(f"shelf\\{shelve_name}")
    shelve_dict = shelveFile[f"{shelve_name[0]}"]
    flag = 0
    print(f"\n\033[7m\033[93mProbable Questions for tag {shelve_name}:\033[0m\033[27m")
    for key in shelve_dict:
        value = shelve_dict.get(key, 0)
        ans = value[0]
        topictags = value[1]
        if len(ans) > 1:
            flag = 1
            print("\033[7m\033[92m")
            pprint.pprint(question[key])
            print("\033[0m\033[27m")
            if key in asked:
                name_list.append((question[key]["title_slug"], key, asked[key], topictags))
            else:
                name_list.append((question[key]["title_slug"], key, topictags))

    if flag == 0:
        print(f"\n\033[7m\033[91mNo questions found for tag {shelve_name}.\033[0m\033[27m")
    return name_list
    # else:
    #     shelveFile = shelve.open(f"{shelve_name}")
    #
    #     shelve_dict = shelveFile[f"{shelve_name[0]}"]
    #     flag = 0
    #     print(f"\n\033[7m\033[93mProbable Questions for tag {shelve_name}:\033[0m\033[27m")
    #     with open(f"result_{shelve_name}.txt", "a") as file:
    #         for key, value in shelve_dict.items():
    #             if len(value) > 1:
    #                 flag = 1
    #                 print("\033[7m\033[92m")
    #                 pprint.pprint(question[key])
    #                 print("\033[0m\033[27m")
    #
    #         if flag == 0:
    #             print(
    #                   f"\n\033[7m\033[91mNo questions found for tag {shelve_name}.\033[0m\033[27m"
    #                   )


if __name__ == '__main__':
    predict.runall()
    tags = this_month_tags.tags
    file_name = get_file()
    name_list = []
    asked = asked_ques()
    for name in tags:
        name_list.append(comp(name, asked))
    with open(file_name, "w") as file:
        file.write("%s%s%s  %s\n" % ("QID".rjust(4),
                                 "Question name ".rjust(60), "Asked Date".rjust(11),"Topics".ljust(60)))
        for ele in name_list:
            if not ele:
                continue
            for ques_name in ele:
                formatted = ''
                value = ques_name[0]
                for word in value.split('-'):
                    if word.startswith('i') and word.endswith('i'):
                        formatted += word.upper() + ' '
                    else:
                        formatted += word.title() + ' '
                if len(ques_name) > 3:
                    topictags = ', '.join(ques_name[-1])
                    file.write("%s%s%s  %s\n" %
                               (str(ques_name[1]).rjust(4),
                                formatted.rjust(60), ques_name[2].rjust(11),
                                topictags.ljust(60)))
                else:
                    topictags = ', '.join(ques_name[-1])
                    file.write("%s%s%s  %s\n" %
                               (str(ques_name[1]).rjust(4), formatted.rjust(60),
                                (" " * 11), topictags.ljust(60)))

