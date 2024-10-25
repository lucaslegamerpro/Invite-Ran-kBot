import discord
from discord.ext import commands
import json

# Configuration du bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Stockage des invitations
guild_invites = {}
invite_counts = {}

def load_invite_data():
    try:
        with open('invite_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_invite_data():
    with open('invite_data.json', 'w') as f:
        json.dump(invite_counts, f)

# Vérification des permissions admin
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté!')
    for guild in bot.guilds:
        guild_invites[guild.id] = await guild.invites()
    global invite_counts
    invite_counts = load_invite_data()

@bot.event
async def on_member_join(member):
    new_invites = await member.guild.invites()
    inviter = None
    
    for invite in new_invites:
        if not any(i.code == invite.code and i.uses < invite.uses for i in guild_invites[member.guild.id]):
            continue
        
        inviter = invite.inviter
        inviter_id = str(inviter.id)
        if inviter_id not in invite_counts:
            invite_counts[inviter_id] = 0
        invite_counts[inviter_id] += 1
        save_invite_data()

        channel = bot.get_channel(ID)
        await channel.send(f"👋 {member.mention} vient de rejoindre!\n"
                         f"➡️ Invité par: {inviter.mention}\n"
                         f"📊 {inviter.mention} a maintenant {invite_counts[inviter_id]} invitations!")

        if invite_counts[inviter_id] == 5:
            role = member.guild.get_role(ID)
            if role:
                await inviter.add_roles(role)
                await channel.send(f"🎉 Félicitations {inviter.mention} ! Tu as atteint 5 invitations et reçois le rôle **{role.name}**!")
        
        break
    
    guild_invites[member.guild.id] = new_invites

@bot.event
async def on_member_remove(member):
    for invite in guild_invites[member.guild.id]:
        if str(invite.inviter.id) in invite_counts:
            channel = bot.get_channel(ID)
            await channel.send(f"👋 **{member.display_name}** vient de quitter le serveur.\n"
                             f"➡️ Il avait été invité par: {invite.inviter.mention}")
            break

@bot.command(name='invites')
async def check_invites(ctx, member: discord.Member = None):
    member = member or ctx.author
    invite_count = invite_counts.get(str(member.id), 0)
    await ctx.send(f"📊 {member.mention} a **{invite_count}** invitations!")

@bot.command(name='give_invites')
@is_admin()
async def give_invites(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("❌ Le nombre d'invitations doit être positif!")
        return
    
    member_id = str(member.id)
    if member_id not in invite_counts:
        invite_counts[member_id] = 0
    
    invite_counts[member_id] += amount
    save_invite_data()
    
    # Vérifier si le membre atteint 5 invitations après l'ajout
    if invite_counts[member_id] >= 5 and (invite_counts[member_id] - amount) < 5:
        role = ctx.guild.get_role(ID)
        if role and role not in member.roles:
            await member.add_roles(role)
            await ctx.send(f"🎉 {member.mention} a reçu le rôle **{role.name}** car il a atteint 5 invitations!")
    
    await ctx.send(f"✅ Ajout de **{amount}** invitation(s) à {member.mention}!\n"
                   f"📊 Total: **{invite_counts[member_id]}** invitation(s)")

@bot.command(name='suppr_invites')
@is_admin()
async def remove_invites(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("❌ Le nombre d'invitations à supprimer doit être positif!")
        return
    
    member_id = str(member.id)
    if member_id not in invite_counts or invite_counts[member_id] < amount:
        await ctx.send("❌ Ce membre n'a pas assez d'invitations à supprimer!")
        return
    
    invite_counts[member_id] -= amount
    save_invite_data()
    
    # Vérifier si le membre passe sous 5 invitations après la suppression
    if invite_counts[member_id] < 5 and (invite_counts[member_id] + amount) >= 5:
        role = ctx.guild.get_role(ID DU ROLE)
        if role and role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"⚠️ {member.mention} a perdu le rôle {role.name} car il est passé sous 5 invitations!")
    
    await ctx.send(f"✅ Suppression de **{amount}** invitation(s) à {member.mention}!\n"
                   f"📊 Total: **{invite_counts[member_id]}** invitation(s)")

# Gestion des erreurs pour les commandes admin
@give_invites.error
@remove_invites.error
async def admin_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ Vous devez être administrateur pour utiliser cette commande!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Usage incorrect! Exemple: `!give_invites @utilisateur 5` ou `!suppr_invites @utilisateur 5`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Membre non trouvé ou nombre invalide!")

bot.run('VOTRE TOKEN DISCORD')
