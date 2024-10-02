import requests
from collections import defaultdict
import os
import sys
import re
import this_month_tags
import shelve


def runall():
    tags = this_month_tags.tags
    index = 0
    if not (os.path.isfile("shelf\\tags.dat"
                           ) and os.path.isfile("shelf\\tags.bak"
                                                ) and os.path.isfile("shelf\\tags.dir")):
        shelfFile = shelve.open("shelf\\tags")
        shelfFile["is_interrupted"] = (False, -1, '')
        shelfFile["is_repeated"] = set()
    else:
        shelfFile = shelve.open("shelf\\tags")
    if shelfFile["is_interrupted"][0]:
        # print(shelfFile["is_interrupted"][0], shelfFile["is_interrupted"][1], shelfFile["is_interrupted"][2])
        print(f"\n\ncontinuing from {shelfFile['is_interrupted'][2]}...")
        index = shelfFile["is_interrupted"][1]
    repeat_set = shelfFile["is_repeated"]
    shelfFile.close()
    # print(repeat_set)
    for i in range(index, len(tags)):
        run(tags[i], i, repeat_set)

    shelfFile = shelve.open("shelf\\tags")
    shelfFile["is_interrupted"] = (False, -1, '')
    shelfFile["is_repeated"] = set()
    shelfFile.close()


def run(this_week_tag, tag_number, repeat_set):
    regobj_editorial = re.compile(r'.*?canSeeDetail.*?(\w+).*', re.S)
    regobj_question = re.compile(r'{.*?frontendQuestionId.*?(\w+).*?titleSlug.*?([\w-]+).*?}', re.S)
    base_url = "https://leetcode.com/graphql"

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
                }
            }
        }""",
        "variables": {"categorySlug": "", "skip": 0, "limit": -1, "filters": {"tags": f"{this_week_tag}"}}
    }

    req = requests.post(base_url, json=data)
    mo = regobj_question.findall(req.text)
    # print(mo)
    question_dict = {}
    if __name__ != '__main__':
        if not (os.path.isfile(f"shelf\\{this_week_tag}.dat"
                               ) and os.path.isfile(f"shelf\\{this_week_tag}.bak"
                                                    ) and os.path.isfile(f"shelf\\{this_week_tag}.dir")):
            shelfFile = shelve.open(f"shelf\\{this_week_tag}")
            shelfFile[f"{this_week_tag[0]}"] = defaultdict(set)
            shelfFile["is_interrupted"] = (False, 0, '')
        else:
            shelfFile = shelve.open(f"shelf\\{this_week_tag}")
    else:
        if not (os.path.isfile(f"{this_week_tag}.dat"
                               ) and os.path.isfile(f"{this_week_tag}.bak"
                                                    ) and os.path.isfile(f"{this_week_tag}.dir")):
            shelfFile = shelve.open(f"{this_week_tag}")
            shelfFile[f"{this_week_tag[0]}"] = defaultdict(set)
            shelfFile["is_interrupted"] = (False, 0, '')
        else:
            shelfFile = shelve.open(f"{this_week_tag}")

    val_dict = shelfFile[f"{this_week_tag[0]}"]
    is_interrupted = shelfFile["is_interrupted"]

    if is_interrupted[0]:
        index = mo.index((is_interrupted[1], is_interrupted[2]))
        mo = mo[index:]
    for key, val in mo[:]:
        question_dict[int(key)] = val
    for key, value in question_dict.items():
        if key in repeat_set:
            continue
        else:
            repeat_set.add(key)
        try:
            data = {
                "query": """query editorialMeta($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                solution {
                    canSeeDetail
                        }
                    }
                }""",
                "variables": {"titleSlug": f"{value}"}
            }
            req = requests.post(base_url, json=data)
            mo = regobj_editorial.findall(req.text)
            ans = 1 if mo and mo[0] == 'true' else 0
            formatted = ''
            for word in value.split('-'):
                if word.startswith('i') and word.endswith('i'):
                    formatted += word.upper() + ' '
                else:
                    formatted += word.title() + ' '

            print(key, formatted)
            val_dict[key].add(ans)
        except (KeyboardInterrupt, ConnectionError):
            print("\nKeyboardInterrupt...progress saved")
            if __name__ != '__main__':
                shelfFile_tags = shelve.open("shelf\\tags")
                shelfFile_tags["is_interrupted"] = (True, tag_number, this_week_tag)
                shelfFile_tags["is_repeated"] = repeat_set
                shelfFile_tags.close()

            shelfFile["is_interrupted"] = (True, str(key), value)
            shelfFile[f"{this_week_tag[0]}"] = val_dict
            shelfFile.close()
            sys.exit(1)
    # print(repeat_set)
    shelfFile["is_interrupted"] = (False, -1, '')
    shelfFile[f"{this_week_tag[0]}"] = val_dict
    shelfFile.close()


if __name__ == '__main__':
    tag = "array"
    run(tag, 0, set())
    import compare
    compare.comp(tag)
