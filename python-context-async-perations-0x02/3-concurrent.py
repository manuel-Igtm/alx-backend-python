import asyncio
import aiomysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Immamanu1234!',
    'db': 'ALX_prodev'
}

async def async_fetch_users():
    async with aiomysql.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM user_data")
            result = await cursor.fetchall()
            print("All Users:", result)
            return result

async def async_fetch_older_users():
    async with aiomysql.connect(**DB_CONFIG) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM user_data WHERE age > %s", (40,))
            result = await cursor.fetchall()
            print("Users Older Than 40:", result)
            return result

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
