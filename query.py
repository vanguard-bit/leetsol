import requests
import question_dict

data = {
    "query": """query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
      difficulty
      frontendQuestionId: questionFrontendId
      paidOnly: isPaidOnly
      titleSlug
      topicTags {
        name
      }
      hasSolution
    }
  }
}""",
    "variables": {"categorySlug": "", "skip": 0, "limit": -1, "filters": {}}
}

req = requests.post("https://leetcode.com/graphql", json=data)
print(req.text[:100])
