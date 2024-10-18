import requests

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
      }}
        }
    }""",
    "variables": {"categorySlug": "", "skip": 0, "limit": -1, "filters": {"tags": "array"}}
}

req = requests.post("https://leetcode.com/graphql", json=data)
print(req.text)
