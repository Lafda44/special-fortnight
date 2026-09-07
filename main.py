import discord
import asyncio
import random
import logging
import sys

# ==========================================================
# CONFIGURATION
# ==========================================================

TOKEN = "MTQ5MjQwMTM2OTEyMDkwMzE3OQ.G6-CFo.NWgf94MfwZatkYV8g3ymgSVuvzfJ4vhWZE97ag"
CHANNEL_ID = 1443835825459826760

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("KataBump")


# ==========================================================
# SELF BOT
# ==========================================================

class UltraSelfBot(discord.Client):

    def __init__(self):
        super().__init__(self_bot=True)

    async def on_ready(self):
        print("=" * 50)
        print(f"Logged in as: {self.user}")
        print(f"Watching channel: {CHANNEL_ID}")
        print("=" * 50)

        self.loop.create_task(self.bump_loop())

    async def bump_loop(self):
        await self.wait_until_ready()

        channel = self.get_channel(CHANNEL_ID)

        if channel is None:
            logger.error("Could not find channel.")
            return

        while not self.is_closed():

            try:
                logger.info("Fetching slash commands...")

                # Fetch commands
                slash_commands = await channel.application_commands()

                # Find /bump
                bump_command = None

                for command in slash_commands:
                    if command.name == "bump":
                        bump_command = command
                        break

                if bump_command:

                    typing_delay = random.uniform(8, 15)

                    logger.info(
                        f"Typing simulation for {typing_delay:.2f} seconds..."
                    )

                    async with channel.typing():
                        await asyncio.sleep(typing_delay)

                    # Execute command
                    await bump_command(channel)

                    logger.info("/bump sent successfully.")

                else:
                    logger.error("/bump command not found.")

                # Wait 10 minutes + random delay
                wait_time = 600 + random.randint(10, 30)

                logger.info(
                    f"Sleeping for {wait_time} seconds..."
                )

                await asyncio.sleep(wait_time)

            except discord.Forbidden:
                logger.error("403 Forbidden.")

                await asyncio.sleep(600)

            except discord.LoginFailure:
                logger.error("Invalid token.")

                break

            except Exception as error:
                logger.error(f"Loop error: {error}")

                await asyncio.sleep(600)


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    client = UltraSelfBot()

    try:
        client.run(TOKEN)

    except Exception as error:
        logger.error(f"Startup error: {error}")
