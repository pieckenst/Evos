#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.utils import get
from discord.ext import commands
from PIL import Image,ImageFont,ImageDraw
import sqlite3
import asyncio
import io
import os
from logging_files.guild_log import logger

def check_channel(author,channel):
    def inner_check(message):
        return len(message.channel_mentions) == 1 and message.author == author and message.channel.id == channel

    return inner_check

def check_autorole(author,channel):
    def inner_check(message):
        return len(message.role_mentions) == 1 and message.author == author and message.channel.id == channel
    
    return inner_check

def check_prefix(author,channel):
    def inner_check(message):
        return len(message.content) <= 3 and message.author == author and message.channel.id == channel
    
    return inner_check

def check_message(author,channel):
    def inner_check(message):
        return message.author == author and message.channel.id == channel

    return inner_check
    
class Guild(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name = "Wlmessage",brief = "Yeni gelen üyeler için karşılama mesajı gönderir.",aliases = ["wlmessage"])
    @commands.has_permissions(administrator=True)
    async def member_welcome_command(self,ctx):
        """Welcome message for newcomers
        Use of : wlmessage
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin kanalı belirleyelim.\n`Belirlemek istediğin kanalı etiketlemen yeterli.`")
        
        try:
            channelSelection = await self.client.wait_for('message',check = check_channel(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        
        else :
            db = sqlite3.connect('data/server/Data.db')
            cursor = db.cursor()
            try :
                channelID = channelSelection.channel_mentions[0].id
                cursor.execute(f"UPDATE ServerData SET WELCOME_CHANNEL_ID = {channelID} WHERE SERVER_ID = {ctx.author.guild.id}")
                db.commit()
                
                await ctx.send(f"Harika! :partying_face: Artık {channelSelection.channel_mentions[0].mention} kanalında yeni üyeler için bilgilendirme mesajı gönderilecek.")
                
                logger.info(f"Guild | Wlmessage | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as e:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")         
                
                logger.error(f"Guild | Wlmessage | Error: {e}")
                pass
            finally :
                cursor.close()
                db.close()

    @commands.command(name = "Lvmessage",brief = "Ayrılan üyeler için bilgilendirme mesajı gönderir.",aliases = ["lvmessage"])
    @commands.has_permissions(administrator=True)
    async def member_leave_command(self,ctx):
        """Information message for leaving members
        Use of : lvmessage
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin kanalı belirleyelim.\n`Belirlemek istediğin kanalı etiketlemen yeterli.`")
        
        try:
            channelSelection = await self.client.wait_for('message',check = check_channel(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        
        else :
            db = sqlite3.connect('data/server/Data.db')
            cursor = db.cursor()
            try :
                channelID = channelSelection.channel_mentions[0].id
                cursor.execute(f"UPDATE ServerData SET LEAVE_CHANNEL_ID = {channelID} WHERE SERVER_ID = {ctx.author.guild.id}")
                db.commit()
                
                await ctx.send(f"Harika! :partying_face: Artık {channelSelection.channel_mentions[0].mention} kanalında ayrılan üyeler için bilgilendirme mesajı gönderilecek.")
                
                logger.info(f"Guild | Lvmessage | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as e:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
                logger.error(f"Guild | Lvmessage | Error: {e}")
                pass
            finally :
                cursor.close()
                db.close()

    @commands.command(name = "Setautorole",brief = "Yeni gelen üyeler için otomatik rol verir.",aliases = ["setautorole"])
    @commands.has_permissions(administrator=True)
    async def autorole_command(self,ctx):
        """Automatic role for newcomers
        Use of : setautorole
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin rolü belirleyelim.\n`Belirlemek istediğin rolü etiketlemen yeterli.`")      
        
        try:
            roleSelection = await self.client.wait_for('message',check = check_autorole(ctx.author,ctx.message.channel.id) ,timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        
        else :
            db = sqlite3.connect('data/server/Data.db')
            cursor = db.cursor()
            try :
                roleID = roleSelection.role_mentions[0].id
                cursor.execute(f"UPDATE ServerData SET AUTOROLE_ID = {roleID} WHERE SERVER_ID = {ctx.author.guild.id}")
                db.commit()
                
                await ctx.send(f"Harika! :partying_face: Artık yeni gelen üyelere {roleSelection.role_mentions[0].mention} rolü verilecek.\n`Uyarı: Evos'un bu işlevi tam olarak yerine getirebilmesi için roller kısmından Evos'un rolünü {roleSelection.role_mentions[0]} rolünden en az 1 kademe üstüne taşıman gerekli.`")
                
                logger.info(f"Guild | Autorole | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as e:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
                logger.error(f"Guild | Autorole | Error: {e}")
                pass
            finally :
                cursor.close()
                db.close()

    @commands.command(name = "ChangePrefix",brief = "Evos'un komut ön ekini değiştirir.",aliases = ["changeprefix"])
    @commands.has_permissions(administrator=True)
    async def change_prefix_command(self,ctx):
        """Change Prefix
        Use of : changeprefix
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nSeçmek istediğin komut ön ekini belirleyelim.\n`Maksimum 3 karakter olmasını ve son karakterinde işaret bulundurmanızı öneriyoruz.`")     
        
        try:
            prefixSelection = await self.client.wait_for('message',check = check_prefix(ctx.author,ctx.message.channel.id) ,timeout=60)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        
        else :
            db = sqlite3.connect('data/server/Data.db')
            cursor = db.cursor()
            try :
                cursor.execute(f"UPDATE ServerData SET CUSTOM_PREFIX = {prefixSelection.content} WHERE SERVER_ID = {ctx.author.guild.id}")
                db.commit()
                
                await ctx.send(f"Harika! :partying_face: Bu sunucu için komut ön eki **{prefixSelection.content}** olarak ayarlandı.")
                
                logger.info(f"Guild | Prefix | Sunucu : {ctx.guild.name} | Tarafından : {ctx.author}")
            except Exception as e:
                await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
                logger.error(f"Guild | ChangePrefix | Error: {e}")
                pass

    @commands.command(name = "ResetConfig",brief = "Sunucu ayarlarını sıfırlar.",aliases = ["resetconfig"])
    @commands.has_permissions(administrator=True)
    async def server_config_reset_command(self,ctx):
        """Reset Server Config
        Use of : resetconfig
        """
        db = sqlite3.connect('data/server/Data.db')
        cursor = db.cursor()
        db2 = sqlite3.connect('data/server/Config.db')
        cursor2 = db2.cursor()
        try :
            cursor.execute(f"UPDATE ServerData SET CUSTOM_PREFIX = '.',AUTOROLE_ID = NULL,WELCOME_CHANNEL_ID = NULL,LEAVE_CHANNEL_ID = NULL WHERE SERVER_ID = {str(ctx.author.guild.id)}")
            db.commit()
            cursor.close()
            db.close()
            
            cursor2.execute(f"DELETE FROM AutoMessage WHERE SERVER_ID = {str(ctx.author.guild.id)}")
            db2.commit()
            
            await ctx.send(f"Harika! :partying_face: Bu sunucunun tüm ayarları sıfırlandı. Prefix(komut ön eki) varsayılan **.(nokta)** olarak ayarlandı.")
        except Exception as e:
            await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
            logger.error(f"Guild | ResetServerConfig | Error: {e}")
            pass
        finally :
            cursor2.close()
            db2.close()

    @commands.command(name = "Automessage",brief = "İstediğiniz kanala otomatik mesaj gönderir.",aliases = ["automessage"])
    @commands.has_permissions(administrator=True)
    async def auto_message_scheduler_command(self,ctx):
        """Auto Message Scheduler
        Use of : automessage
        """
        await ctx.send(f"Selam {ctx.author.mention}!\nÖnce istediğin duyurmak istediğin mesajı belirleyelim.\n`Mesajının maksimum 512 karakter olmasını öneriyoruz.`")     
        
        try:
            messageSelection = await self.client.wait_for('message',check = check_message(ctx.author,ctx.message.channel.id) ,timeout=300)
        except asyncio.TimeoutError:
            await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
        
        else :
            await ctx.send(f"Harika! :partying_face: Şimdi bu mesajın kaç saatte bir yayınlanmasını gerektiğini belirleyelim.\n`Sadece tam sayı girişi yapman gerekir. Aksi taktirde bu sistem çalışmayacaktır.`")           
            
            try:
                timeSelection = await self.client.wait_for('message',check = check_message(ctx.author,ctx.message.channel.id) ,timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(f":sleeping: {ctx.author.mention} Belirlenen sürede senden herhangi bir yanıt alamadık.")
            
            else :
                db = sqlite3.connect('data/server/Config.db')
                cursor = db.cursor()
                try :
                    cursor.execute(f"INSERT INTO AutoMessage VALUES ('{str(ctx.message.guild.id)}','{str(ctx.message.channel.id)}','{str(messageSelection.content)}',{int(timeSelection.content)},{int(timeSelection.content)})")
                    db.commit()

                    await ctx.send(f"Harika! :partying_face: Artık bu kanalda her **{timeSelection.content}** saatte bir mesajın yayınlanacak.")             
                    
                    logger.info(f"Guild | AutoMessage | Sunucu : {ctx.guild.name} | Mesaj : {messageSelection.content} |Tarafından : {ctx.author}")
                except Exception as e:
                    await ctx.send(":thinking: Görünüşe göre şu anda sunucu kayıtlarına ulaşamıyoruz.Daha sonra tekrar deneyebilirsin.")
                
                    logger.error(f"Guild | AutoMessage | Error: {e}")
                    pass
                finally :
                    cursor.close()
                    db.close()

    @commands.Cog.listener()
    async def on_member_join(self,member):
        db = sqlite3.connect('data/server/Data.db')
        cursor = db.cursor()
        
        try :
            cursor.execute(f"SELECT AUTOROLE_ID,WELCOME_CHANNEL_ID FROM ServerData WHERE SERVER_ID = {member.guild.id}")
            data = cursor.fetchone()

            if data[0] != None :
                autoRoleID = data[0]
                autoRole = discord.utils.get(member.guild.roles, id=int(autoRoleID))
                
                if autoRole != None :                  
                    try :
                        await member.add_roles(autoRole)
                    except :
                        pass

            if data[1] is not None :
                channelID = data[1]
                channel = discord.utils.get(member.guild.text_channels, id=int(channelID))
                
                if channel != None :
                    welcomeImg = Image.open("./images/info-background.jpg")
                    draw = ImageDraw.Draw(welcomeImg)
                    W = 1920
                    defaultSize = 80
                    if len(member.guild.name)>50 :
                        defaultSize -= len(member.guild.name) - 25
 
                    headerFont = ImageFont.truetype("./assets/fonts/SansitaSwashed-VariableFont_wght.ttf", 150)
                    defaultFont = ImageFont.truetype("./assets/fonts/Oxanium-Regular.ttf", defaultSize)
                    
                    headerMessage = "HOŞGELDİN"
                    countMemberMessage = f"{member.guild.name} | {len(member.guild.members)}.ÜYE"

                    w,h = draw.textsize(headerMessage,font=headerFont)

                    draw.text(((W-w)/2,50), headerMessage, (255, 255, 255), font=headerFont)
                    w,h = draw.textsize(countMemberMessage,font=defaultFont)
                    draw.text(((W-w)/2,900), countMemberMessage, (255, 255, 255), font=defaultFont)

                    member_avatar_asset = member.avatar_url_as(format='jpg', size=512)
                    member_buffer_avatar = io.BytesIO(await member_avatar_asset.read())

                    member_image = Image.open(member_buffer_avatar)
                    member_image = member_image.resize((512, 512))

                    circle_image = Image.new('L', (512, 512))
                    circle_draw = ImageDraw.Draw(circle_image)
                    circle_draw.ellipse((0, 0, 512, 512), fill=255)

                    welcomeImg.paste(member_image, (704, 300), circle_image)
                    welcomeImg.save(f"{member.id}.png")
                    
                    await channel.send(f"Hoşgeldin, {member.mention}!",file=discord.File(f"{member.id}.png"))

                    os.remove(f"{member.id}.png")
        except Exception as e:

            logger.error(f"Guild | Data | Error: {e}")
            pass
        finally :
            cursor.close()
            db.close()

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        db = sqlite3.connect('data/server/Data.db')
        cursor = db.cursor()
        
        if member.name != self.client.user.name :

            try :
                cursor.execute(f"SELECT LEAVE_CHANNEL_ID FROM ServerData WHERE SERVER_ID = {member.guild.id}")
                data = cursor.fetchone()

                if data[0] != None :
                    channelID = data[0]
                    channel = discord.utils.get(member.guild.text_channels, id=int(channelID))
                
                    if channel != None :
                        leaveImg = Image.open("./images/info-background.jpg")
                        draw = ImageDraw.Draw(leaveImg)
                        W = 1920
                        defaultSize = 80
                        if len(member.guild.name)>50 :
                            defaultSize -= len(member.guild.name) - 25
 
                        headerFont = ImageFont.truetype("./assets/fonts/SansitaSwashed-VariableFont_wght.ttf", 150)
                        defaultFont = ImageFont.truetype("./assets/fonts/Oxanium-Regular.ttf", defaultSize)
                    
                        headerMessage = "GÜLE GÜLE"
                        countMemberMessage = f"{member.guild.name} | {len(member.guild.members)} ÜYE"

                        w,h = draw.textsize(headerMessage,font=headerFont)

                        draw.text(((W-w)/2,50), headerMessage, (255, 255, 255), font=headerFont)
                        w,h = draw.textsize(countMemberMessage,font=defaultFont)
                        draw.text(((W-w)/2,900), countMemberMessage, (255, 255, 255), font=defaultFont)

                        member_avatar_asset = member.avatar_url_as(format='jpg', size=512)
                        member_buffer_avatar = io.BytesIO(await member_avatar_asset.read())

                        member_image = Image.open(member_buffer_avatar)
                        member_image = member_image.resize((512, 512))

                        circle_image = Image.new('L', (512, 512))
                        circle_draw = ImageDraw.Draw(circle_image)
                        circle_draw.ellipse((0, 0, 512, 512), fill=255)

                        leaveImg.paste(member_image, (704, 300), circle_image)
                        leaveImg.save(f"{member.id}.png")
                    
                        await channel.send(f"{member.mention}, aramızdan ayrıldı!",file=discord.File(f"{member.id}.png"))

                        os.remove(f"{member.id}.png")
            except Exception as e:

                logger.error(f"Guild | Data | Error: {e}")
                pass
            finally :
                cursor.close()
                db.close()
  
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = sqlite3.connect('data/server/Data.db')
        cursor = db.cursor()
        
        try :
            cursor.execute(f"DELETE FROM ServerData WHERE SERVER_ID = {str(guild.id)}")
            cursor.execute(f"INSERT INTO ServerData VALUES ('{str(guild.id)}','.',NULL,NULL,NULL)")
            db.commit()
            
            infoEmbed = discord.Embed(title = "Evos'u sunucuna eklediğin için teşekkürler!",colour=0xd8f500)
            infoEmbed.add_field(name="Prefix (Özelleştirilebilir)",value="Varsayılan: **.**(Nokta)",inline=False)
            infoEmbed.add_field(name="Komut Listesi",value="Komutları görmek için **.yardım** yazabirsin.",inline=False)
            infoEmbed.add_field(name="Geliştirici misin ?",value="[Buradan](https://github.com/semihaydin0/Evos) kaynak kodlarını inceleyebilirsin.",inline=False)
            infoEmbed.set_footer(text="PHOENIX#7103 tarafından 💖 ile geliştirildi!",icon_url=guild.icon_url)
            file = discord.File("images/evos.png", filename="evos.png")
            infoEmbed.set_thumbnail(url="attachment://evos.png")
            
            try :
                await guild.text_channels[0].send(file=file,embed=infoEmbed)
            except :
                pass
        except Exception as e:

            logger.error(f"Guild | Data | Error: {e}")
            pass
        finally :
            cursor.close()
            db.close()

def setup(client):
    client.add_cog(Guild(client))