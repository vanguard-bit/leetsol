import requests
import re

req = requests.get("https://leetcode.com/api/problems/all/")

regobj = re.compile(r'.*?\"question__article__live\".*?(\w+).*?\"question__article__slug.*?.*?([\w-]+).*?question__title_slug.*?([\w-]+).*?frontend_question_id.*?(\d+).*?difficulty.*?level.*?(\d+).*?paid_only.*?(\w+).*?}')
"""
group 1: has editorial? if not null
group 2: editorial slug if not null
group 3: title slug
group 4: frontend_question_id
group 5: difficulty
group 6: paid_only
"""

mo = regobj.findall(req.text)

dif = {
    '1': "Easy",
    '2': "Medium",
    '3': "Hard"
}

file_content = """question = {
"""
ques_struct = """    %s: {
        'title_slug': \'%s\',
        'hasEditorial': %s,
        'editorial_slug': \'%s\',
        'difficulty': \'%s\',
        'isPaid': %s
    },
"""

for block in mo:
    has_editorial = block[0]
    has_editorial = True if has_editorial == 'true' else False

    editorial_slug = block[1]
    title_slug = block[2]
    frontend_qid = block[3]
    difficulty = dif[block[4]]

    ispaid = block[5]
    ispaid = True if ispaid == 'true' else False
    file_content += ques_struct % (
        frontend_qid, title_slug, has_editorial, editorial_slug, difficulty, ispaid
    )

file_content = file_content[:-2] + '\n}\n'
# print(file_content)
with open("question_dict.py", "w") as file:
    file.write(file_content)
# print(i, sum, len(mo) / 2)
# print(file_content)


if __name__ == '__main__':
    import question_dict
    print(len(question_dict.question))
