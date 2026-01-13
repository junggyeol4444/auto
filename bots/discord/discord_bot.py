"""
디스코드 봇 메인 모듈
Discord Bot Main Module with comprehensive features
"""
import discord
from discord.ext import commands
import asyncio
import logging
from datetime import datetime
import json
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('discord_bot')


class DiscordBot:
    """디스코드 봇 메인 클래스"""
    
    def __init__(self, token=None):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.token = token
        self.is_running = False
        
        # 자동 응답 키워드
        self.auto_responses = {
            '안녕': '안녕하세요! 무엇을 도와드릴까요?',
            '도움': '명령어 목록: !안녕, !날씨, !주사위, !투표, !음악재생',
            '도움말': '명령어 목록: !안녕, !날씨, !주사위, !투표, !음악재생'
        }
        
        # 욕설 리스트 (간단한 예시)
        self.bad_words = ['욕설1', '욕설2', '비속어']
        
        # 스팸 감지 설정
        self.spam_threshold = 5  # 5초 내 5개 메시지
        self.user_message_times = {}
        
        self.setup_events()
        self.setup_commands()
    
    def setup_events(self):
        """이벤트 핸들러 설정"""
        
        @self.bot.event
        async def on_ready():
            logger.info(f'{self.bot.user} 봇이 준비되었습니다!')
            self.is_running = True
            await self.bot.change_presence(
                activity=discord.Game(name="!도움 입력")
            )
        
        @self.bot.event
        async def on_member_join(member):
            """새 멤버 환영 메시지"""
            channel = member.guild.system_channel
            if channel:
                embed = discord.Embed(
                    title="🎉 새로운 멤버!",
                    description=f'{member.mention}님, 환영합니다!',
                    color=discord.Color.green()
                )
                await channel.send(embed=embed)
                logger.info(f'새 멤버 가입: {member.name}')
        
        @self.bot.event
        async def on_message(message):
            if message.author.bot:
                return
            
            # 스팸 감지
            if await self.check_spam(message):
                try:
                    await message.author.timeout(
                        datetime.timedelta(minutes=5),
                        reason="스팸 감지"
                    )
                    await message.channel.send(
                        f'{message.author.mention} 스팸으로 감지되어 5분간 뮤트되었습니다.'
                    )
                    logger.warning(f'스팸 감지: {message.author.name}')
                except:
                    pass
            
            # 욕설 감지
            if any(bad_word in message.content for bad_word in self.bad_words):
                await message.delete()
                await message.channel.send(
                    f'{message.author.mention} 부적절한 언어 사용이 감지되었습니다. 경고!'
                )
                logger.warning(f'욕설 감지: {message.author.name}')
            
            # 자동 응답
            for keyword, response in self.auto_responses.items():
                if keyword in message.content:
                    await message.channel.send(response)
                    break
            
            await self.bot.process_commands(message)
    
    async def check_spam(self, message):
        """스팸 메시지 감지"""
        user_id = message.author.id
        current_time = datetime.now().timestamp()
        
        if user_id not in self.user_message_times:
            self.user_message_times[user_id] = []
        
        # 최근 메시지 시간 추가
        self.user_message_times[user_id].append(current_time)
        
        # 5초 이전 메시지 제거
        self.user_message_times[user_id] = [
            t for t in self.user_message_times[user_id] 
            if current_time - t < 5
        ]
        
        # 스팸 감지
        return len(self.user_message_times[user_id]) >= self.spam_threshold
    
    def setup_commands(self):
        """명령어 설정"""
        
        @self.bot.command(name='안녕')
        async def hello(ctx):
            """안녕하세요 명령어"""
            await ctx.send(f'안녕하세요, {ctx.author.mention}님!')
        
        @self.bot.command(name='날씨')
        async def weather(ctx, *, city: str = '서울'):
            """날씨 정보 (간단한 더미 데이터)"""
            embed = discord.Embed(
                title=f'🌤️ {city} 날씨',
                description='맑음, 기온 15°C',
                color=discord.Color.blue()
            )
            embed.add_field(name='습도', value='60%', inline=True)
            embed.add_field(name='풍속', value='2m/s', inline=True)
            await ctx.send(embed=embed)
        
        @self.bot.command(name='주사위')
        async def dice(ctx, sides: int = 6):
            """주사위 굴리기"""
            import random
            result = random.randint(1, sides)
            await ctx.send(f'🎲 주사위 결과: {result}')
        
        @self.bot.command(name='투표')
        async def poll(ctx, *, question):
            """투표 생성"""
            embed = discord.Embed(
                title='📊 투표',
                description=question,
                color=discord.Color.gold()
            )
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
            await message.add_reaction('👎')
        
        @self.bot.command(name='핑')
        async def ping(ctx):
            """봇 응답 속도"""
            latency = round(self.bot.latency * 1000)
            await ctx.send(f'🏓 Pong! 지연시간: {latency}ms')
        
        @self.bot.command(name='정보')
        async def info(ctx):
            """서버 정보"""
            guild = ctx.guild
            embed = discord.Embed(
                title=f'📌 {guild.name} 서버 정보',
                color=discord.Color.purple()
            )
            embed.add_field(name='멤버 수', value=guild.member_count, inline=True)
            embed.add_field(name='채널 수', value=len(guild.channels), inline=True)
            embed.add_field(name='역할 수', value=len(guild.roles), inline=True)
            embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
            await ctx.send(embed=embed)
        
        @self.bot.command(name='청소')
        @commands.has_permissions(manage_messages=True)
        async def clear(ctx, amount: int = 10):
            """메시지 삭제 (관리자 전용)"""
            await ctx.channel.purge(limit=amount + 1)
            msg = await ctx.send(f'✅ {amount}개의 메시지를 삭제했습니다.')
            await asyncio.sleep(3)
            await msg.delete()
        
        @self.bot.command(name='킥')
        @commands.has_permissions(kick_members=True)
        async def kick(ctx, member: discord.Member, *, reason='없음'):
            """멤버 킥 (관리자 전용)"""
            await member.kick(reason=reason)
            await ctx.send(f'👢 {member.mention}님을 킥했습니다. 사유: {reason}')
            logger.info(f'킥: {member.name}, 사유: {reason}')
        
        @self.bot.command(name='밴')
        @commands.has_permissions(ban_members=True)
        async def ban(ctx, member: discord.Member, *, reason='없음'):
            """멤버 밴 (관리자 전용)"""
            await member.ban(reason=reason)
            await ctx.send(f'🔨 {member.mention}님을 밴했습니다. 사유: {reason}')
            logger.info(f'밴: {member.name}, 사유: {reason}')
    
    def run(self):
        """봇 실행"""
        if not self.token:
            logger.error('토큰이 설정되지 않았습니다.')
            return False
        
        try:
            self.bot.run(self.token)
            return True
        except Exception as e:
            logger.error(f'봇 실행 오류: {str(e)}')
            self.is_running = False
            return False
    
    async def start_async(self):
        """비동기 봇 시작"""
        if not self.token:
            logger.error('토큰이 설정되지 않았습니다.')
            return
        
        try:
            await self.bot.start(self.token)
        except Exception as e:
            logger.error(f'봇 시작 오류: {str(e)}')
            self.is_running = False
    
    async def stop(self):
        """봇 중지"""
        await self.bot.close()
        self.is_running = False
        logger.info('봇이 중지되었습니다.')


if __name__ == '__main__':
    # 테스트용
    bot = DiscordBot()
    print("디스코드 봇 모듈이 로드되었습니다.")
