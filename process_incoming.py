import requests
import json
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib


def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })

    embedding = r.json()['embeddings']
    return embedding

df = joblib.load('embeddings.joblib')

incoming_query = input("Ask a Question:")
Question_embedding = create_embedding([incoming_query])[0]


similarities = cosine_similarity(np.vstack(df['embedding']),[Question_embedding]).flatten()
# print(similarities)
top_results = 10
max_indx = similarities.argsort()[::-1][0:top_results]
# print(max_indx)
new_df = df.loc[max_indx]
# print(new_df[[ "number", "text"]])

prompt = f'''I am teaching web development using Sigma web development course. here are vedio
subtitle chunks containing video title, vedio number, start time in seconds, end time in seconds,
the text at the time:

{new_df[["title", "number", "start", "end", "text"]].to_json()}

--------------------------------
"{incoming_query}"
user ask this question related to this vedio chunks, you have to answer where and how much
content is taught in which vedio (in which vedio and at whatv timetamp) and guide the user to go 
to that particular vedio. if user asks unrelated question, tell him that you can only answer
question related to the course.

'''
with open("prompt.text", "w") as f:
    f.write(prompt)



# for index, item in new_df.iterrows():
#     print (index, item["title"], item["number"], item["text"], item["start"],"-" , item["end"])
    
