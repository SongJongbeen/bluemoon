from discord.utils import get

async def toggle_role(member, role_name):
    role = get(member.guild.roles, name=role_name)
    
    if role is None:
        return False, "역할이 존재하지 않습니다."
        
    if role in member.roles:
        await member.remove_roles(role)
        return True, f"{member.mention}님에게서 '{role_name}' 역할을 제거했습니다."
    else:
        await member.add_roles(role)
        return True, f"{member.mention}님에게 '{role_name}' 역할을 부여했습니다."
