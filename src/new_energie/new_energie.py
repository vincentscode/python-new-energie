from __future__ import annotations

import asyncio
import json
import socket
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, List, cast

import async_timeout
from aiohttp import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import NewEnergieConnectionError
from .models import Contract, Product

if TYPE_CHECKING:
    from typing_extensions import Self

@dataclass
class NewEnergie:
    session: ClientSession
    host: str = "meine.new-energie.de"
    request_timeout: float = 10.0
    _close_session: bool = False

    async def _request(self, uri: str, *, method: str = METH_GET, data: dict[str, Any] | None = None) -> Any:
        url = URL.build(scheme="https", host=self.host, path="/portal/api/").join(URL(uri))

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en-DE;q=0.9,en;q=0.8,de-DE;q=0.7,de;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'X-COS-UA': 'default',
            'X-XSRF-TOKEN': 'fa65d3b6-f00e-454b-89c0-e439f576d7d9',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    json=data,
                    headers=headers,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = f"Timeout occurred while connecting to {self.host}"
            raise NewEnergieConnectionError(msg) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = f"Error occurred while communicating with {self.host}"
            raise NewEnergieConnectionError(msg) from exception

        return cast(dict[str, Any], json.loads(await response.text()))

    async def login(self, token: str) -> None:
        self.session.cookie_jar.update_cookies({
            'cos-oidc-token': token,
            'new_openid_token': token,
            'cookietest': '1',
        })

    async def contracts(self) -> List[Contract]:
        data = await self._request("b2c/contract-overview")
        assert "contractAccounts" in data, "Invalid response"
        assert len(data["contractAccounts"]) > 0, "No contract accounts found"
        assert len(data["contractAccounts"]) == 1, "Multiple contract accounts are not supported"
        contract_account = data["contractAccounts"][0]

        assert "contracts" in contract_account, "Invalid response"

        contracts = []
        for contract_data in contract_account["contracts"]:
            contract = Contract.from_dict(contract_data)
            contracts.append(contract)
        
        return contracts
    
    async def products(self) -> List[Product]:
        contracts = await self.contracts()

        products = []
        for contract in contracts:
            products.append(contract.product)

        return products


    async def close(self) -> None:
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        await self.close()
