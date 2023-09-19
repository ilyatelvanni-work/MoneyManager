import traceback
import json

from decorator import decorator

from MoneyManager.Account import Account
from MoneyManager.Category import Category
from MoneyManager.Currency import Currency
from MoneyManager.Transaction import Transaction
from MoneyManager.db_connection import get_session

# from TES_roleplaying_system.character import Client as CharactersClient
# from TES_roleplaying_system.dialog import Client as DialogsClient


@decorator
async def prepare_api_response(async_func, *args, **kwargs):
    try:
        return json.dumps({
            'error': None,
            'response': await async_func(*args, **kwargs)}, default=lambda o: o.__json__()
        )
    except Exception as err:
        traceback.print_exc()
        return json.dumps({'error': str(err), 'response': None})


class API:

    def __init__(self):
        # self.characters_client = CharactersClient()
        # self.dialogs_client = DialogsClient()
        pass

    @prepare_api_response
    async def get_currency(self):
        return await Currency.get()

    @prepare_api_response
    async def get_category(self):
        return await Category.get()

    @prepare_api_response
    async def get_account(self):
        return await Account.get()

    @prepare_api_response
    async def create_transaction(self, *args, **kwargs):
        return await Transaction.create(*args, **kwargs)




    # @prepare_api_response
    # async def api_get_character_by_id(self, id_: int):
    #     return await self.characters_client.get_character_by_id(id_)

    # @prepare_api_response
    # async def get_chain_of_messages_for_character(self, character_id: int):
    #     return await self.dialogs_client.get_chain_of_messages_for_character(character_id)

    # @prepare_api_response
    # async def send_message_for_character(self, character_id: int, message: str):
    #     return await self.dialogs_client.send_message_for_character(character_id, message)


if __name__ == '__main__':

    import asyncio

    from TES_roleplaying_system.db_connection import init_engine

    async def main():
        await init_engine()
        print(await API().api_get_character_by_id(1))

    asyncio.run(main())
