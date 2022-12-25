import discord
import urllib.request
import requests
import math
import random
from googleapiclient.discovery import build

from discord.ext import commands
from youtubesearchpython import VideosSearch
from discord import ui
from discord.commands import Option
import googletrans
from mojang import API
translator = googletrans.Translator()
youtube = build('youtube', 'v3', 
                developerKey='ss')
bot = commands.Bot(command_prefix = '+',intents=discord.Intents.all())
token = '토큰'

api = API()



from googlesearch import search





@bot.event
async def on_ready():
        print('test')
        




        
@bot.slash_command(description="마크 스킨, uuid를 조회하고 그 값을 반환합니다")
async def 마인크래프트검색(ctx, 닉네임: Option(str, "닉네임을 입력하세요!"),):
    uuid = api.get_uuid(f"{닉네임}")
    embed=discord.Embed(title=f"{ctx.author.name}님의 마인크래프트 검색 결과입니다!", color=0x0067a3)
    embed.set_thumbnail(url=f"https://minotar.net/cube/{닉네임}/100.png")
    embed.set_image(url=f"https://minotar.net/armor/body/{닉네임}/100.png")
    embed.add_field(name= f"uuid:",value=f" {uuid}", inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command(description="ping!")
async def 핑(ctx):
    embed=discord.Embed(title="🏓 퐁!", description=f"**{round(bot.latency *1000)}** ms의 시간이 지연되었네요!", color=0xff0000)
    await ctx.respond(embed=embed)


@bot.slash_command(description="마크 서버 상태를 반환합니다. 그 값이 유효하지 않다면 사진이 도출되지 않습니다.")
async def 마인크래프트서버검색(ctx, 서버이름: Option(str, "검색할 서버 이름을 입력하세요!"), 아이피: Option(str, "검색할 서버 아이피 입력하세요!"), 포트: Option(str, "검색할 서버 포트를 입력하세요!"),):
    author = ctx.author.name
    embed=discord.Embed(title=f"{author}님의 마인크래프트 서버 검색 결과입니다!", color=0x0067a3)
    embed.set_image(url=f"http://status.mclive.eu/{서버이름}/{아이피}/{포트}/banner.png")
    await ctx.respond(embed=embed)



@bot.slash_command(description="번역합니다")
async def 번역(ctx, to: Option(str, "번역 할 언어를 고르세요!.(코드로, ex | 한국=ko / 미국=en..)"), 말: Option(str, "번역 할 말을 쓰세요!"),):
    str1 = f"{말}"
    result1 = translator.translate(str1, dest=f'{to}')
    
    g_hex = random.randint(0, 255)

    embed = discord.Embed(title=f"**번역 결과**", description=f"", color=discord.Color.from_rgb(0, g_hex, 255))
    embed.add_field(name= "from:",value=f"{말}", inline=True)
        
    embed.add_field(name= "to:",value=f"{to}", inline=True)
    
    embed.add_field(name= "결괏값:",value=f"{result1.text}", inline=True)
    

    await ctx.respond(embed=embed)
    




@bot.slash_command(description="유튜브에 내용을 검색합니다")
async def 유튜브검색(ctx, 채널: Option(str, "유튜브에 검색 할 채널의 이름을 입력하세요. (/c/뒤에 붙은 태그 혹은 핸들에서 @를 제외한 값)"),):
    #https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q={채널}&type=channel&key=AIzaSyDLlay6_8BDIxq5gjhwbIqnqRsY5HTHZKE
    yt = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q={채널}&type=channel&key=AIzaSyDLlay6_8BDIxq5gjhwbIqnqRsY5HTHZKE')

    yt_j = yt.json()
    d= yt_j["items"][0]["snippet"]["thumbnails"]["default"]["url"]
    c = yt_j["items"][0]["snippet"]["description"]
    b = yt_j["items"][0]["snippet"]["title"]

    a = yt_j["items"][0]["id"]["channelId"]

    ch_request = youtube.channels().list(
    part='statistics',
    id=a)
    # Channel Information
    ch_response = ch_request.execute()
  
    sub = ch_response['items'][0]['statistics']['subscriberCount']
    vid = ch_response['items'][0]['statistics']['videoCount']
    views = ch_response['items'][0]['statistics']['viewCount']
  
    print("Total Subscriber:- ", sub)
    print("Total Number of Videos:- ", vid)
    print("Total Views:- ", views)
    g_hex = random.randint(0, 255)

    embed = discord.Embed(title=f"**닉네임 : {b}**", description=f"**설명 : {c}**, ", color=discord.Color.from_rgb(0, g_hex, 255))

    embed.set_thumbnail(url=d)
    embed.add_field(name= "구독자:",value=f" {sub}", inline=True)
    embed.add_field(name= "영상의 수: ",value=f"{vid}", inline=True)
    embed.add_field(name= "총 조회수: ",value=f"{views}", inline=True)
    embed.add_field(name= "아이디: ",value=f"{a}", inline=True)
    

    youtube.channels().list(part="id", forUsername="Nyaneo")

    view = ui.View()
    view.add_item(ui.Button(label='채널 바로가기', url=f'https://www.youtube.com/channel/{a}', row=0))
    await ctx.respond(embed=embed,view=view)

    #f"**{b}**\n{c} {d} \n 구독자: {sub}, 영상의 수: {vid}, 총 조회수: {views}"



@bot.slash_command(description="한강의 온도를 검색합니다")
async def 한강온도(ctx):
    hangang = requests.get('https://api.hangang.msub.kr/')
    hangang_C = hangang.json()
    g_hex = random.randint(0, 255)
    embed = discord.Embed(title=f"💧 한강 수온 : **{hangang_C['temp']}°C**", description=f"**{hangang_C['station']}**, **{hangang_C['time']}**", color=discord.Color.from_rgb(0, g_hex, 255))
    embed.set_footer(text="msub 한강 api 사용")
    await ctx.respond(embed=embed)

@bot.slash_command(description="도움말을 검색합니다")
async def 도움말(ctx):
    g_hex = random.randint(0, 255)
    embed = discord.Embed(title=f"**도움말**", description=f"네온봇은 디스코드 서버에 실용성을 더해주는 참신한 봇입니다!\n내 서버안의 작은 스마트폰, 네온봇", color=discord.Color.from_rgb(0, g_hex, 255))

    embed.add_field(name= "제작자",value=f"Flag\_Fan\nEdeep\_", inline=True)
    view = ui.View()
    view.add_item(ui.Button(label='깃허브 바로가기', url='https://github.com/Neon-Bots', row=0))
    await ctx.respond(embed=embed,view=view)






    


@bot.slash_command(description="실시간 코로나 현황을 검색합니다")
async def 코로나(ctx):
    crn_json = requests.get('https://capi.msub.kr/')
    crn = crn_json.json()
    chex = random.randint(0, 255)
    embed = discord.Embed(title=f"코로나 정보", description=f"**{crn['update']}**", color=discord.Color.from_rgb(255, 0, chex))
    embed.add_field(name=":flag_kr: 총 확진자", value=".", inline=True)
    embed.add_field(name=f"{crn['accumulate']['confirmation']}명", value=f"(+{crn['today']['confirmation']})", inline=True)
    embed.add_field(name=f"{crn['accumulate']['dead']}명", value=f"(+{crn['today']['dead']})", inline=True)

    embed.add_field(name=":flag_kr: 오늘 확진자", value=".", inline=True)
    embed.add_field(name=f"{crn['today']['confirmation']}", value="오늘 확진자 수", inline=True)
    embed.add_field(name=f"{crn['today']['dead']}", value="오늘 사망자 수", inline=True)
    embed.set_footer(text="msub Corona api 사용")
    await ctx.respond(embed=embed)
    
from currency_converter import CurrencyConverter
c = CurrencyConverter()


@bot.slash_command(description="환율 변환..!")
async def 환율변환기(ctx, 가격:Option(str, "가격을 작성해주세요!(숫자만)"), from돈:Option(str, "작성", choices=["유로", "달러", "원화"]), to돈:Option(str, "작성", choices=["유로", "달러", "원화"]),):
    option = 가격
    rkqt1 = from돈
    rkqt2 = to돈

    if rkqt1 == "유로":
        if rkqt2 == "달러" :
            i = c.convert(가격,'EUR','USD')
            
            await ctx.respond(f"{round(i, 2)}달러입니다!") #round(num, 3)

    if rkqt1 == "달러":
        if rkqt2 == "유로" :
            i = c.convert(가격,'USD','EUR')
            await ctx.respond(f"{round(i, 2)}유로입니다!")

    if rkqt1 == "원화":
        if rkqt2 == "달러" :
            i = c.convert(가격,'KRW','USD')
            await ctx.respond(f"{round(i, 2)}달러입니다!")

    if rkqt1 == "원화":
        if rkqt2 == "유로" :
            i = c.convert(가격,'KRW','EUR')
            await ctx.respond(f"{round(i, 2)}유로입니다!")


    if rkqt1 == "유로":
        if rkqt2 == "원화" :
            i = c.convert(가격,'EUR','KRW')
            await ctx.respond(f"{round(i,2)}원입니다!")

    if rkqt1 == "달러":
        if rkqt2 == "원화" :
            i = c.convert(가격,'USD','KRW')
            await ctx.respond(f"{round(i,2)}원입니다!")





        



@bot.slash_command(description="계산기, 파이는 파이로 입력하고 e 는 e 로 입력해주세요!")
async def 계산기(ctx, 옵션:Option(str, "단위 옵션을 선택해주세요!", choices=["루트", "사인", "코사인", "탄젠트", "제곱", "팩토리얼", "덧셈", "뺄셈", "나눗셈", "곱셈"]), 값1, 값2):
    option = 옵션
    rkqt1 = 값1
    rkqt2 = 값2

    
    if option == "루트":
        if rkqt1 == "파이":
            await ctx.respond(f'결과는 {math.sqrt(math.pi)} 입니다!')
        elif rkqt1 == "e":
            await ctx.respond(f'결과는 {math.sqrt(math.e)} 입니다!')
        else:
            await ctx.respond(f'결과는 {math.sqrt(int(rkqt1))} 입니다!')
            
    elif option == "사인":
        if rkqt1 == "파이":
            await ctx.respond(f'결과는 {math.sin(math.pi)} 입니다!')
        elif rkqt1 == "e":
            await ctx.respond(f'결과는 {math.sin(math.e)} 입니다!')
        else:
            await ctx.respond(f'결과는 {math.sin(int(rkqt1))} 입니다!')
            
    elif option == "코사인":
        if rkqt1 == "파이":
            await ctx.respond(f'결과는 {math.cos(math.pi)} 입니다!')
        elif rkqt1 == "e":
            await ctx.respond(f'결과는 {math.cos(math.e)} 입니다!')
        else:
            await ctx.respond(f'결과는 {math.cos(int(rkqt1))} 입니다!')

    elif option == "탄젠트":
        if rkqt1 == "파이":
            await ctx.respond(f'결과는 {math.tan(math.pi)} 입니다!')
        elif rkqt1 == "e":
            await ctx.respond(f'결과는 {math.tan(math.e)} 입니다!')
        else:
            await ctx.respond(f'결과는 {math.tan(int(rkqt1))} 입니다!')
            
    elif option == "제곱":
        if rkqt1 == "파이":
            if rkqt2 == "파이":
                await ctx.respond(f'결과는 {math.pow(math.pi, math.pi)} 입니다!')
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 {math.pow(math.pi, math.e)} 입니다!')
            else:
                await ctx.respond(f'결과는 {math.pow(math.pi, int(rkqt1))} 입니다!')
        elif rkqt1 == "e":
            if rkqt2 == "파이":
                await ctx.respond(f'결과는 {math.pow(math.e, math.pi)} 입니다!')
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 {math.pow(math.e, math.e)} 입니다!')
            else:
                await ctx.respond(f'결과는 {math.pow(math.e, int(rkqt1))} 입니다!')
        else:
            await ctx.respond(f'결과는 {math.pow(int(rkqt1), int(rkqt2))} 입니다!')

    elif option == "팩토리얼":
        if rkqt1 == "파이":
            await ctx.respond("소수점은 불가능합니다.", ephemeral=True)
        elif rkqt1 == "e":
            await ctx.respond("소수점은 불가능합니다.", ephemeral=True)
        else:
            print(math.factorial(int(rkqt1)))
            await ctx.respond(f'결과는 {math.factorial(int(rkqt1))} 입니다!')

    elif option == "덧셈":
        if rkqt1 == "파이":
            if rkqt2 == "파이":
                await ctx.respond(f'결과는 {math.pi + math.pi} 입니다!')
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 {math.pi + math.e} 입니다!')
            else:
                await ctx.respond(f'결과는 {math.pi + int(rkqt1)} 입니다!')
        elif rkqt1 == "e":
            if rkqt2 == "파이":
                await ctx.respond(f'결과는 {math.e + math.pi} 입니다!')
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 {math.e + math.e} 입니다!')
            else:
                await ctx.respond(f'결과는 {math.e + int(rkqt1)} 입니다!')
        else:
            await ctx.respond(f'결과는 {int(rkqt1) + int(rkqt2)} 입니다!')

    elif option == "뺄셈":
        if rkqt1 == "파이":
            if rkqt2 == "파이":
                await ctx.respond(0)
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 {math.pi - math.e} 입니다!')
            else:
                await ctx.respond(f'결과는 {math.pi - int(rkqt1)} 입니다!')
        elif rkqt1 == "e":
            if rkqt2 == "파이":
                await ctx.respond(f'결과는 {math.e - math.pi} 입니다!')
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 0 입니다!')
            else:
                await ctx.respond(f'결과는 {math.e - int(rkqt1)} 입니다!')
        else:
            await ctx.respond(f'결과는 {int(rkqt1) - int(rkqt2)} 입니다!')

    elif option == "곱셈":
        if rkqt1 == "파이":
            if rkqt2 == "파이":
                await ctx.respond(f'결과는 {math.pi * math.pi} 입니다!')
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 {math.pi * math.e} 입니다!')
            else:
                await ctx.respond(f'결과는 {math.pi * int(rkqt1)} 입니다!')
        elif rkqt1 == "e":
            if rkqt2 == "파이":
                await ctx.respond(f'결과는 {math.e * math.pi} 입니다!')
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 {math.e * math.e} 입니다!')
            else:
                await ctx.respond(f'결과는 {math.e * int(rkqt1)} 입니다!')
        else:
            await ctx.respond(f'결과는 {int(rkqt1) * int(rkqt2)} 입니다!')

    elif option == "나눗셈":
        if rkqt1 == "파이":
            if rkqt2 == "파이":
                await ctx.respond(f'결과는 {math.pi / math.pi} 입니다!')
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 {math.pi / math.e} 입니다!')
            else:
                await ctx.respond(f'결과는 {math.pi / int(rkqt1)} 입니다!')
        elif rkqt1 == "e":
            if rkqt2 == "파이":
                await ctx.respond(f'결과는 {math.e / math.pi} 입니다!')
            elif rkqt2 == "e":
                await ctx.respond(f'결과는 {math.e / math.e} 입니다!')
            else:
                await ctx.respond(f'결과는 {math.e / int(rkqt1)} 입니다!')
        else:
            await ctx.respond(f'결과는 {int(rkqt1) / int(rkqt2)} 입니다!')







bot.run(token)
