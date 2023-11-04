import json
import urllib.request
import sqlite3

connection = sqlite3.connect('data.db')


def send_request(prompt):
    data = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [{
            "role": "user",
            "content": prompt
        }]
    }).encode()

    request = urllib.request.Request(
        'https://api.openai.com/v1/chat/completions',
        method="POST",
        headers={
            "Content-type": "application/json",
            "Authorization": "Bearer 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"
        },
        data=data
    )

    response = urllib.request.urlopen(request)
    json_response = json.loads(response.read())

    return json_response["choices"][0]["message"]["content"]


def create_table():
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "prompts" (
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "prompt" TEXT NOT NULL,
            "response" TEXT NOT NULL,
            "created_at" TIMESTAMP NOT NULL
            )
    ''')

    connection.commit()


def insert_prompt(prompt, response):
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO "prompts" ("prompt", "response", "created_at") VALUES (?,?, DATETIME('now'))
    ''', (prompt, response))
    connection.commit()

    return cursor.lastrowid


def update_prompt(prompt, response):
    cursor = connection.cursor()

    cursor.execute('''
    UPDATE "prompts" SET "response" = ? WHERE "prompt" = ?
    ''', (response, prompt))
    connection.commit()


def in_database(prompt):
    cursor = connection.cursor()

    cursor.execute('''
        SELECT "response" FROM "prompts" WHERE "prompt" = ?
        ''', [prompt])

    return cursor.fetchone()


def response_from_database(id_response):
    cursor = connection.cursor()

    cursor.execute('''
        SELECT "response" FROM "prompts" WHERE "id" = ?
        ''', [id_response])

    return cursor.fetchone()


def main():
    create_table()
    while True:
        prompt = input('Enter a prompt: ')

        if prompt == "exit":
            break

        response_from_db = in_database(prompt)

        if response_from_db is None:
            response_from_chat = send_request(prompt)
            last_inserted_id = insert_prompt(prompt, response_from_chat)

            response_from_db = response_from_database(last_inserted_id)

        print(f'Response: {response_from_db}')

        response_rating = input('Do you like the response if you dont like it write NO')
        if response_rating.lower() == 'no':
            response_from_chat = send_request(prompt)
            update_prompt(prompt, response_from_chat)

            print(f'Regenerated response: {response_from_chat}')


if __name__ == '__main__':
    main()
