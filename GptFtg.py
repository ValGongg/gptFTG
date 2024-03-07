# requires: openai
from .. import loader, utils
import openai

@loader.tds
class PromptMod(loader.Module):
    """Prompts the ChatGPT API's GPT-3.5 model with user's arguments"""
    strings = {"name": "ChatGPT"}

    async def client_ready(self, client, db):
        self.db = db

    async def promptcmd(self, message):
        """Prompts the ChatGPT API's GPT-3.5 model with user's arguments"""
        args = utils.get_args_raw(message)
        context = await message.get_reply_message()

        if not args:
            await utils.answer(message, "Please provide some text to prompt the ChatGPT API's GPT-3.5 model with.")
            return

        api_key = self.db.get(__name__, "openai_api_key", None)

        if not api_key:
            await utils.answer(message, "No OpenAI API key found. Please set one with .setaikey <key>.")
            return

        await utils.answer(message, "Тупое ебланище, жди, я думаю")

        openai.api_key = api_key

        if context is not None:
            completion = await utils.run_sync(openai.ChatCompletion.create,
                model="gpt-3.5-turbo",
                messages=[
                   {"role": "user", "content": context},
                    {"role": "user", "content": args}
                ]
            )
        else:
            completion = await utils.run_sync(openai.ChatCompletion.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": args}
                ]
            )

        await utils.answer(message, completion.choices[0].message.content)

    async def setaikeycmd(self, message):
        """Sets the OpenAI API key"""
        key = utils.get_args_raw(message)

        if not key:
            await utils.answer(message, "Please provide an OpenAI API key.")
            return

        self.db.set(__name__, "openai_api_key", key)
        await utils.answer(message, "OpenAI API key set.")
