import question_dict


class Question:
    def __init__(self, problem: dict, val):
        self.question_slug = problem['title_slug']
        self.qid = val
        self.isPaid = problem['isPaid']
        self.difficulty = problem['difficulty']
        self.name = self.get_name()

    def get_name(self):
        temp = ''
        for ele in self.question_slug.split('-'):
            temp += chr(ord(ele[0]) - 32) + ele[1:] + ' '

        return temp

    def get_link(self):
        return f"https://leetcode.com/problems/{self.question_slug}/description/"

    def __str__(self):
        return f"""\nProblem Name: {self.name}\nProblem Number: {self.qid}\nProblem Difficulty: {self.difficulty}\nPremium Only?: {self.isPaid}\n"""


val = input("Feeling bored? Enter a random number in range 1 to 3000: ")
if val.isdigit() and 1 <= int(val) <= 3000:
    int(val)
    problem = Question(question_dict.question[val], val)
else:
    import random
    print("Wrong entry randomizing choice...\n")
    val = random.randint(1, 3000)
    problem = Question(question_dict.question[val], val)
print("Here solve this problem\n", problem.get_link(), sep='')
print(problem)


