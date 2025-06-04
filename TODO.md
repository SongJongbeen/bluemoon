# To Do
[*] 유튜브 노래 재생

# 시간 반복
[*] (가능하면) 필드보스/결계 알람
[*] 심구알람

# 크롤링 관련
마비노기 모바일 공지 크롤링 + AI 요약

# TTS 관련
[*] 음성 채팅방에 누가 들어왔는지 이름을 불러주는 tts
[*] 특정 채팅채널의 메시지를 읽어주는 tts

# 완료
[*] 명단/캐릭터검색
[*] 오늘의 운세
[*] (퍼플렉시티 써서) 마비노기 모바일 QnA 챗봇? -> 가끔 잘못된 정보를 줄 수 있음
[*] 사다리타기

---
노래가 너무 길어서 못 재생할때 메세지 전송

Traceback (most recent call last):
  File "C:\Users\20200\miniconda3\envs\bluemoon\Lib\site-packages\discord\ext\commands\core.py", line 235, in wrapped
    ret = await coro(*args, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\cursor\bluemoon\cogs\play_music.py", line 63, in play
    await ctx.send(f"'{info['title']}'을(를) 큐에 추가했습니다.")
                       ~~~~^^^^^^^^^
TypeError: 'coroutine' object is not subscriptable

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\20200\miniconda3\envs\bluemoon\Lib\site-packages\discord\ext\commands\bot.py", line 1366, in invoke
    await ctx.command.invoke(ctx)
  File "C:\Users\20200\miniconda3\envs\bluemoon\Lib\site-packages\discord\ext\commands\core.py", line 1029, in invoke
    await injected(*ctx.args, **ctx.kwargs)  # type: ignore
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\20200\miniconda3\envs\bluemoon\Lib\site-packages\discord\ext\commands\core.py", line 244, in wrapped
    raise CommandInvokeError(exc) from exc
discord.ext.commands.errors.CommandInvokeError: Command raised an exception: TypeError: 'coroutine' object is not subscriptable
