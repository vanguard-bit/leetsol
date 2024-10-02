import shelve
import predict
import this_month_tags
import pprint
from question_dict import question


def comp(shelve_name):
    if __name__ == '__main__':
        shelveFile = shelve.open(f"shelf\\{shelve_name}")
    else:
        shelveFile = shelve.open(f"{shelve_name}")

    shelve_dict = shelveFile[f"{shelve_name[0]}"]
    flag = 0
    print(f"\n\033[7m\033[93mProbable Questions for tag {shelve_name}:\033[0m\033[27m")
    for key, value in shelve_dict.items():
        if len(value) > 1:
            flag = 1
            print("\033[7m\033[92m")
            pprint.pprint(question[key])
            print("\033[0m\033[27m")

    if flag == 0:
        print(f"\n\033[7m\033[91mNo questions found for tag {shelve_name}.\033[0m\033[27m")


if __name__ == '__main__':
    predict.runall()
    tags = this_month_tags.tags
    for name in tags:
        comp(name)


