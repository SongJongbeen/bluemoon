def is_user_joined_channel(before, after, target_channel_id):
    """
    사용자가 특정 음성채널에 새로 입장했는지 판별
    """
    # before.channel이 None(음성채널에 없었음), after.channel이 target 채널이면 입장
    return before.channel is None and after.channel and after.channel.id == target_channel_id

def make_join_message(member):
    """
    음성채널 입장 메시지 생성
    """
    return f"{member.display_name} 님이 음성채널에 입장했습니다."

async def join_voice_channel(bot, guild, channel_id):
    """
    봇이 지정한 음성채널에 입장
    """
    channel = guild.get_channel(channel_id)
    if channel is None or not hasattr(channel, "connect"):
        if channel is None:
            print("channel is None")
        return False  # 음성채널이 아님 또는 존재하지 않음

    # 이미 연결되어 있으면 이동, 아니면 새로 연결
    voice_client = guild.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.move_to(channel)
    else:
        await channel.connect()
    return True

async def leave_voice_channel(guild):
    """
    봇이 음성채널에서 퇴장
    """
    voice_client = guild.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        return True
    return False
