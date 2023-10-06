import asyncio
import aiohttp

from new_energie import NewEnergie, Contract

token = '<enter token here>'


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        async with NewEnergie(session=session) as client:
            await client.login(token)
            products = await client.products()
            for product in products:
                print(product.description)
                for price in product.prices:
                    print(" -", price.name, price.net, "/", price.gross, price.unit)

if __name__ == "__main__":
    asyncio.run(main())
