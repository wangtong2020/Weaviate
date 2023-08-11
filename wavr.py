import weaviate
import pandas as pd
import codecs

import json
# 定义client
client = weaviate.Client(url='https://my-sandebox-tdq1b7h0.weaviate.network')

class_obj = {
    "class": "Stephen_Chow",
    "properties": [
        {
            'name': 'title',
            'dataType': ['text'],
        },
        {
            'name': 'author',
            'dataType': ['text'],
        },
        {
            'name': 'body',
            'dataType': ['text'],
        },
    ],
    "vectorizer": "text2vec-openai",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    "moduleConfig": {
        "text2vec-openai": {},
        "generative-openai": {}  # Ensure the `generative-openai` module is used for generative queries
    }
}
response = client.schema.get("Stephen_Chow")

# Load data

with codecs.open('test-dataset-2.md', 'r', encoding='utf-8') as file:
    markdown_text1 = file.read()
with codecs.open('test-dataset-1.md', 'r', encoding='utf-8') as file:
    markdown_text2 = file.read()
data1 = markdown_text1
data2 = markdown_text2
# Configure a batch process
with client.batch(
    batch_size=100
) as batch:
    # Batch import all Questions
    for i, d in enumerate(data1):
        print(f"importing article1: {i+1}")
    for i, d in enumerate(data2):
        print(f"importing article2: {i+1}")

response = (
    client.query
    .get("Stephen_Chow", ["author", "body"])
    .with_near_text({
        "concepts": ["新诤信知识产权"]
    })
    .with_limit(2)
    .with_additional(["distance"])
    .do()
)

print(json.dumps(response, indent=2))


