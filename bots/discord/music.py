"""
디스코드 음악 봇 모듈
Music bot with YouTube playback support
"""
import discord
from discord.ext import commands
import asyncio
import logging

logger = logging.getLogger('music_bot')


class MusicBot:
    """음악 재생 봇 클래스"""
    
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}  # 서버별 재생 목록
        self.now_playing = {}  # 현재 재생 중인 곡
        self.setup_commands()
    
    def setup_commands(self):
        """음악 관련 명령어 설정"""
        
        @self.bot.command(name='join')
        async def join(ctx):
            """음성 채널 입장"""
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                if ctx.voice_client is None:
                    await channel.connect()
                    await ctx.send(f'🎵 {channel.name}에 입장했습니다!')
                else:
                    await ctx.voice_client.move_to(channel)
                    await ctx.send(f'🎵 {channel.name}로 이동했습니다!')
            else:
                await ctx.send('❌ 먼저 음성 채널에 입장해주세요!')
        
        @self.bot.command(name='leave')
        async def leave(ctx):
            """음성 채널 퇴장"""
            if ctx.voice_client:
                await ctx.voice_client.disconnect()
                await ctx.send('👋 음성 채널에서 나갔습니다!')
                # 큐 초기화
                if ctx.guild.id in self.queues:
                    self.queues[ctx.guild.id] = []
            else:
                await ctx.send('❌ 음성 채널에 연결되어 있지 않습니다!')
        
        @self.bot.command(name='play')
        async def play(ctx, *, url):
            """음악 재생 (YouTube URL)"""
            await ctx.send(
                f'🎵 음악 재생 기능은 yt-dlp와 FFmpeg가 설치되어야 합니다.\n'
                f'URL: {url}\n'
                f'실제 구현 시 yt-dlp로 다운로드 후 재생합니다.'
            )
            
            # 실제 구현 예시 (yt-dlp 필요):
            # try:
            #     import yt_dlp
            #     
            #     if not ctx.voice_client:
            #         if ctx.author.voice:
            #             await ctx.author.voice.channel.connect()
            #         else:
            #             await ctx.send('❌ 먼저 음성 채널에 입장해주세요!')
            #             return
            #     
            #     ydl_opts = {
            #         'format': 'bestaudio/best',
            #         'postprocessors': [{
            #             'key': 'FFmpegExtractAudio',
            #             'preferredcodec': 'mp3',
            #             'preferredquality': '192',
            #         }],
            #     }
            #     
            #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #         info = ydl.extract_info(url, download=False)
            #         url2 = info['url']
            #         title = info['title']
            #     
            #     FFMPEG_OPTIONS = {
            #         'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            #         'options': '-vn'
            #     }
            #     
            #     ctx.voice_client.stop()
            #     ctx.voice_client.play(
            #         discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS),
            #         after=lambda e: print(f'재생 완료: {title}')
            #     )
            #     
            #     await ctx.send(f'🎵 재생 중: {title}')
            # 
            # except Exception as e:
            #     await ctx.send(f'❌ 오류 발생: {str(e)}')
        
        @self.bot.command(name='pause')
        async def pause(ctx):
            """음악 일시정지"""
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                await ctx.send('⏸️ 일시정지했습니다!')
            else:
                await ctx.send('❌ 재생 중인 음악이 없습니다!')
        
        @self.bot.command(name='resume')
        async def resume(ctx):
            """음악 재개"""
            if ctx.voice_client and ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                await ctx.send('▶️ 재생을 재개합니다!')
            else:
                await ctx.send('❌ 일시정지된 음악이 없습니다!')
        
        @self.bot.command(name='stop')
        async def stop(ctx):
            """음악 정지"""
            if ctx.voice_client:
                ctx.voice_client.stop()
                await ctx.send('⏹️ 음악을 정지했습니다!')
                # 큐 초기화
                if ctx.guild.id in self.queues:
                    self.queues[ctx.guild.id] = []
            else:
                await ctx.send('❌ 재생 중인 음악이 없습니다!')
        
        @self.bot.command(name='skip')
        async def skip(ctx):
            """다음 곡으로 건너뛰기"""
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send('⏭️ 다음 곡으로 건너뜁니다!')
            else:
                await ctx.send('❌ 재생 중인 음악이 없습니다!')
        
        @self.bot.command(name='queue')
        async def queue(ctx):
            """재생 목록 보기"""
            guild_id = ctx.guild.id
            if guild_id in self.queues and self.queues[guild_id]:
                queue_list = '\n'.join([
                    f'{i+1}. {song}' 
                    for i, song in enumerate(self.queues[guild_id])
                ])
                embed = discord.Embed(
                    title='📜 재생 목록',
                    description=queue_list,
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send('📭 재생 목록이 비어있습니다!')
        
        @self.bot.command(name='nowplaying')
        async def now_playing(ctx):
            """현재 재생 중인 곡"""
            guild_id = ctx.guild.id
            if guild_id in self.now_playing and self.now_playing[guild_id]:
                await ctx.send(f'🎵 현재 재생 중: {self.now_playing[guild_id]}')
            else:
                await ctx.send('❌ 재생 중인 음악이 없습니다!')
        
        @self.bot.command(name='volume')
        async def volume(ctx, vol: int = None):
            """볼륨 조절 (0-100)"""
            if vol is None:
                await ctx.send('🔊 사용법: !volume <0-100>')
                return
            
            if not 0 <= vol <= 100:
                await ctx.send('❌ 볼륨은 0-100 사이의 값이어야 합니다!')
                return
            
            if ctx.voice_client and ctx.voice_client.source:
                ctx.voice_client.source.volume = vol / 100
                await ctx.send(f'🔊 볼륨을 {vol}%로 설정했습니다!')
            else:
                await ctx.send('❌ 재생 중인 음악이 없습니다!')


if __name__ == '__main__':
    print("음악 봇 모듈이 로드되었습니다.")
