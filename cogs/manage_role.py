import discord
from discord.ext import commands
from utils.roles import toggle_role

ROLES = {
    "필보": "필보",
    "결계": "결계",
    "심구": "심구"
}

class RoleButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="필보", style=discord.ButtonStyle.primary)
    async def pilbo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        success, message = await toggle_role(interaction.user, ROLES["필보"])
        await interaction.response.send_message(message, ephemeral=True)

    @discord.ui.button(label="결계", style=discord.ButtonStyle.primary)
    async def gyeolgye_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        success, message = await toggle_role(interaction.user, ROLES["결계"])
        await interaction.response.send_message(message, ephemeral=True)

    @discord.ui.button(label="심구", style=discord.ButtonStyle.primary)
    async def simgu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        success, message = await toggle_role(interaction.user, ROLES["심구"])
        await interaction.response.send_message(message, ephemeral=True)

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_role_message(self, channel):
        """역할 버튼 메시지를 전송하는 함수"""
        view = RoleButtonView()
        return await channel.send("아래 버튼을 눌러 필요한/제거할 역할을 클릭하세요!", view=view)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def togglerole(self, ctx, member: discord.Member, role_name: str):
        """특정 유저의 역할을 토글 (필보/결계/심구)"""
        if role_name not in ROLES:
            await ctx.send("유효하지 않은 역할입니다. '필보', '결계', '심구' 중에서 선택해주세요.")
            return
            
        success, message = await toggle_role(member, ROLES[role_name])
        await ctx.send(message)

    @commands.command(name='역할')
    async def rolebutton(self, ctx):
        """버튼을 눌러 '테스트' 역할을 토글할 수 있는 메시지 전송"""
        await self.send_role_message(ctx.channel)

async def setup(bot):
    await bot.add_cog(RoleManager(bot))
