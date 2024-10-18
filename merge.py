import requests
import shelve
import re
import this_month_tags


def req(this_week_tag):
    data = {
            "query": """query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                    problemsetQuestionList: questionList(
                    categorySlug: $categorySlug
                    limit: $limit
                    skip: $skip
                    filters: $filters
              ){
                total: totalNum
                questions: data {
                    frontendQuestionId: questionFrontendId
                    titleSlug
                    topicTags {
                        name
                        }
                    }
                }
            }""",
            "variables": {"categorySlug": "", "skip": 0, "limit": -1, "filters": {"tags": f"{this_week_tag}"}}
    }

    base_url = "https://leetcode.com/graphql"
    req = requests.post(base_url, json=data)
    return req.text


def regex_find(_ele):
    req_text = req(_ele)
    regobj_question = re.compile(
            r'{.*?frontendQuestionId.*?(\w+).*?titleSlug.*?([\w-]+).*?\"topicTags\".*?\[(.*?)\]\}',
            re.S)
    mo = regobj_question.findall(req_text)
    tagreg = re.compile(r'\"name\".*?\"(.*?)\"}', re.S)
    for i in range(len(mo)):
        mo[i] = list(mo[i])
        ele = mo[i]
        mo[i][2] = tagreg.findall(ele[2])
        mo[i] = tuple(mo[i])
    # print(mo[0])
    extract = {}
    for ele in mo:
        extract[int(ele[0])] = ele[2]
    # print(extract)
    file = shelve.open(f'shelf\\{_ele}')
    file_dict = file[_ele[0]]
    # print(file_dict.values())
    # print(file_dict)
    for key, val in file_dict.items():
        popped = val.pop()
        new_val = popped[1]
        val_set = popped[0]
        # print(val_set, new_val)
        file_dict[key] = [val_set, new_val]
    for key, value in file_dict.items():
        print(key, value)
    file[_ele[0]] = file_dict
    file.close()
    # print(file['a'])
    return mo


# regex_find('array')
