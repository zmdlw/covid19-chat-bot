import asyncio
import discord
from discord import message
import requests
from discord.ext import commands
from bs4 import BeautifulSoup
import datetime
bot = discord.Client()

# 생성된 토큰을 입력해준다.
token = ""

# 봇이 구동되었을 때 보여지는 코드
@bot.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(bot.user.name)
    print(bot.user.id)
    print("================")


@bot.event
async def on_message(message):
    if message.content.startswith("?코로나"):
        res = requests.get("http://ncov.mohw.go.kr/").text
        soup = BeautifulSoup(res, "html.parser")

        #국내, 해외 발생 리스트
        ko_v = soup.find("div", attrs={"class":"datalist"}).find_all("span", attrs={"class":"data"})
        kov_list = []
        for kov in ko_v:
            kov_list.append(kov.get_text())

        #확진자[0], 격리해제[1], 치료중[2], 사망[3] 리스트
        all_per = soup.find("ul", attrs={"class":"liveNum"}).find_all("span", attrs={"class":"num"})
        all_per_list = []
        for allper in all_per:
            all_per_list.append(allper.get_text().replace("(누적)", ""))

        #전일대비 리스트
        before_per = soup.find("ul", attrs={"class":"liveNum"}).find_all("span", attrs={"class":"before"})
        before_per_list = []
        for beforper in before_per:
            before_per_list.append(beforper.get_text().replace("전일대비 ", ""))

        #최신 브리핑 리스트
        new_briefing = soup.find("ul", attrs={"class":"m_text_list"}).find_all("a")
        new_briefing_list = []
        for briefing in new_briefing:
            new_briefing_list.append(briefing.get_text())    # [0]
            new_briefing_list.append(briefing["href"])    # [1]

        #00월 00일 00시 기준
        whentotaldata = soup.find("span", attrs={"class":"livedate"}).get_text().strip().replace("(", "").replace(")", "").replace(", ", " | ")

        embed = discord.Embed(title="코로나 19 현황", description="", color=0xff0000)
        embed.set_author(name="코로나 바이러스 감염증 - 19 (COVID-19)", url="http://ncov.mohw.go.kr/", icon_url="https://cdn.discordapp.com/attachments/779326874026377226/789094221533282304/Y5Tg6aur.png")
        embed.add_field(name="Last data time", value="**" + whentotaldata + "**", inline=False)
        embed.add_field(name="총 확진환자", value=all_per_list[0] + before_per_list[0] , inline=True)
        embed.add_field(name="완치환자", value=all_per_list[1] + before_per_list[1], inline=True)
        embed.add_field(name="치료 중(격리 중)", value=all_per_list[2] + before_per_list[2], inline=True)
        embed.add_field(name="사망", value=all_per_list[3] + before_per_list[3], inline=True)
        embed.add_field(name="국내발생", value="+ " + kov_list[0], inline=True)
        embed.add_field(name="해외발생", value="+ " + kov_list[1], inline=True)
        embed.add_field(name="최신 브리핑", value="[{}](http://ncov.mohw.go.kr{})".format(new_briefing_list[0], new_briefing_list[1]) + "\n"
                                                + "[{}](http://ncov.mohw.go.kr{})".format(new_briefing_list[2], new_briefing_list[3]) , inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/779326874026377226/789094221533282304/Y5Tg6aur.png")
        embed.set_footer(text="자세한 정보는 위의 프로필 버튼의 사이트를 방문해주세요.", icon_url="https://cdn.discordapp.com/attachments/779326874026377226/789098688315654164/Flag_of_South_Korea.png")
        await message.channel.send(embed=embed)

    if message.author.bot:
        return None

    if message.content.startswith('!message'):
        channel = message.channel
        await channel.send('message')
    
    if message.content.startswith('!message'):
        channel = message.channel
        await channel.send('')

    if message.content.startswith('!message'):
        channel = message.channel
        await channel.send('message')

    if(message.content == "!time"):
        await message.channel.send(embed=discord.Embed(title="Time", timestamp=datetime.datetime.utcnow()))

    bad = ['message', 'message']


    message_contant=message.content
    for i in bad:
        if i in message_contant:
            await message.channel.send('message')
            await message.delete()
    
    if message.content.startswith('message'):
        channel = message.channel
        await channel.send('message')


bot.run(token)
