from openai import OpenAI
import httpx
import csv


def truncate_string(text, max_tokens=1400):

    tokens = text.split()


    if len(tokens) > max_tokens:
        truncated_tokens = tokens[:max_tokens]
        truncated_text = ' '.join(truncated_tokens)
        return truncated_text
    else:
        return text

#data
def read_csv_file(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)

        headers = next(csv_reader)

        data = []

        for row in csv_reader:
            data.append(row)

    return headers, data

file_path = '.\data\modified_issueDataTensorflow_feature3.csv'
headers, data = read_csv_file(file_path)

print("Column heading:", headers)
print("Line number:", len(data))


print('---------------------------------------------------------------------')


for num in range(100):
    chat_history = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    client = OpenAI(
        base_url="https://api.xty.app/v1",
        api_key="......................",
        http_client=httpx.Client(
            base_url="https://api.xty.app/v1",
            follow_redirects=True,
        ),
    )


    for i in range(1):
        #print("circle" + str(i+1))
        #user_message = input("User: ")
        truncated_text = truncate_string(data[num][8])
        user_message1 = truncated_text
        user_message2 = 'Based on the information provided in the post above, the task is to determine whether the issue described is indeed a bug in the tensorflow/tensorflow project itself. If the poster has used the bug label but the provided information does not clearly indicate that the problem is caused by the tensorflow/tensorflow project, it could be due to other reasons such as the poster\'s own code writing errors or compatibility issues with third-party libraries. Therefore, based on the above situation, outputting 1 indicates that the issue may not be a bug in the tensorflow/tensorflow project itself but may be caused by other reasons. Outputting 0 indicates that the issue is likely a bug in the tensorflow/tensorflow project itself. To standardize the output, simply output 0 or 1 without additional information.'

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history + [{"role": "user", "content": user_message1}, {"role": "user", "content": user_message2}]
        )

        #response = completion
        response = completion.choices[0].message.content
        print("OpenAI:", response)

        chat_history.append({"role": "user", "content": user_message1 + user_message2})
        chat_history.append({"role": "system", "content": response})

