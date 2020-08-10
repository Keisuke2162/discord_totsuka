# python3 discordbot.py で実行

# インストールした discord.py を読み込む
import discord
from discord.ext import commands
import asyncio

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzQyMDU2NjAzMzA1Mzc3ODg1.XzAkEA.BCRiZjVj6jJbt0oEFuVIPTbRz1k'

# 接続に必要なオブジェクトを生成
#client = discord.Client()
client = commands.Bot(command_prefix='.')

"""
# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
"""

# メッセージ受信時に動作する処理
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


async def on_message(message):
    #  /makechecker でアンケート開始
    if message.content == '/neko':
        await client.send_message('ねこ')


@client.command()
async def rect(ctx, about="募集"):
    ok_header = "===参加===\n"
    ng_header = "===不参加===\n"
    #reaction_member = [">>>"]
    ok_member = []
    ng_member = []
    test = discord.Embed(title=about,colour=0x1e90ff)
    test.add_field(name=f"参加者募集中\n", value=ok_header + ng_header, inline=True)
    msg = await ctx.send(embed=test)

    #投票箱
    await msg.add_reaction('🙆‍♂️')
    await msg.add_reaction('🙅‍♂️')
    await msg.add_reaction('⏬')

    #チェック処理
    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '🙆‍♂️' or emoji == '🙅‍♂️' or emoji == '⏬'
    
    while True: 
        reaction, user = await client.wait_for('reaction_add', check=check)

        #参加ボタン
        if str(reaction.emoji) == '🙆‍♂️':
            if user.name in ng_member:
                ng_member.remove(user.name)
            
            if user.name in ok_member:
                ok_member.remove(user.name)
            else:
                ok_member.append(user.name)

            test = discord.Embed(title=about,colour=0x1e90ff)
            test.add_field(name=f"参加者募集中\n", value=ok_header + '\n'.join(ok_member) + '\n' + ng_header + '\n'.join(ng_member), inline=True)
            await msg.edit(embed=test)
            print("add member")
        
        #不参加ボタン
        elif str(reaction.emoji) == '🙅‍♂️':
            if user.name in ok_member:
                ok_member.remove(user.name)
            
            if user.name in ng_member:
                ng_member.remove(user.name)
            else:
                ng_member.append(user.name)

            test = discord.Embed(title=about,colour=0x1e90ff)
            test.add_field(name=f"参加者募集中\n", value=ok_header + '\n'.join(ok_member) + '\n' + ng_header + '\n'.join(ng_member), inline=True)
            await msg.edit(embed=test)
        
        #終了ボタン
        elif str(reaction.emoji) == '⏬':
            print("集計終了")
            break

        await msg.remove_reaction(str(reaction.emoji), user)
    
    print("集計処理を終了しました")

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
