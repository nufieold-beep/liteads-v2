import asyncio
from starlette.background import BackgroundTask
async def foo(a,b,c):
    print(f"a={a}, b={b}, c={c}")
t = BackgroundTask(foo, b='apple', c='banana', a='cat')
asyncio.run(t())