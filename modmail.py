import discord
from discord.ext import commands

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.modmail_channel = None

    @commands.group(name="modmail", invoke_without_command=True)
    async def modmail(self, ctx):
        """
        Main modmail command group
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed. Please use `!modmail help` for a list of commands.")

    @modmail.command(name="setup")
    async def modmail_setup(self, ctx, channel: discord.TextChannel):
        """
        Set the modmail channel
        """
        self.modmail_channel = channel
        await ctx.send(f"Modmail channel set to {channel.mention}")

    @modmail.command(name="close")
    async def modmail_close(self, ctx, ticket_channel: discord.TextChannel):
        """
        Close a modmail ticket
        """
        await ticket_channel.delete()
        await ctx.send("Modmail ticket closed.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None and self.modmail_channel:
            # Message is a DM
            if message.author != self.bot.user:
                # Message is from a user
                category = self.modmail_channel.category
                if category is None:
                    await message.author.send("Modmail system is not set up properly. Please contact an admin.")
                else:
                    ticket_channel = await category.create_text_channel(f"ticket-{message.author.id}")
                    await ticket_channel.send(f"{message.author.mention} ({message.author}): {message.content}")
                    await message.author.send(f"Your message has been sent to the moderation team. They will respond in {ticket_channel.mention}")

bot = commands.Bot(command_prefix="!")
bot.add_cog(ModMail(bot))
bot.run("TOKEN")
