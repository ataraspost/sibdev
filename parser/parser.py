
import asyncio
import json
import copy
import logging

from aiofile import AIOFile, LineReader

from models import User, Precedent, objects


async def save_precedent(user_id, precedent_dict):
    # TODO Этот кусок блокирует event_loop
    id = copy.copy(user_id)
    coppy_precedent = copy.deepcopy(precedent_dict)
    for key in precedent_dict:

        precedent_dict = {
            **coppy_precedent[key],
            'user_id': id,
            'name': key,
        }
        precedent_dict['attitude'] = 1 if precedent_dict['attitude'] == 'positive' else -1
        await objects.create(Precedent, **precedent_dict)



async def line_parser(line, n):

    copy_line = copy.deepcopy(line)
    n_ = copy.copy(n)
    user_dict = {
        'first_name': copy_line['name'].split(' ')[0],
        'last_name': copy_line['name'].split(' ')[1],
        'email': f'fake{n_}@test.ru',
        'password': 'pbkdf2_sha256$216000$0lG5EdRhxjJa$0JF59GxFK79CDo2qqtLkJYvTtHJ88Y+PObAhMCwZDqk=',

    }
    try:
        user = await objects.get(User, email=user_dict['email'])
    except User.DoesNotExist:
        user = await objects.create(User, **user_dict)
    print(f'User saved: {user.id}')
    await save_precedent(user.id, line['precedents'])




async def aenumerate(asequence, start=0):
    n = start
    async for elem in asequence:
        yield n, elem
        n += 1

async def main():
    async with AIOFile('participants.json', 'r') as afp:
        async for n, line in aenumerate(LineReader(afp), 1):
            line_dict = json.loads(line)
            await line_parser(line_dict, n)


asyncio.run(main())

