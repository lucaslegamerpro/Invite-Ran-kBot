# 🤖 Discord Invite Rank Bot

Un bot Discord qui permet de suivre les invitations des membres, avec un système de récompenses automatique et des commandes administratives.

## ✨ Fonctionnalités

- 📊 Suivi automatique des invitations
- 🎯 Attribution automatique de rôle à 5 invitations
- 👋 Messages personnalisés pour les arrivées/départs
- ⚙️ Commandes administratives pour gérer les invitations
- 💾 Sauvegarde permanente des données

## 📋 Prérequis

- Python 3.9 ou supérieur
- Un bot Discord avec les "Privileged Gateway Intents" activés
- Permissions "Gérer le serveur" et "Gérer les rôles" pour le bot

## 🚀 Installation
Hebergez votre bot gratuitement :
rejoignez ce serveur discord : discord.gg/invite/gratuit
aller dans le salon commandes et executer la commende `create-user`, vous allez recevoir vos identifients par mp!!
si ca bloque, aller dans paramètre (discord) cliquer sur confidencialité, serveur puis E-BOT et aitoriser les messages privés, réésayez.
toujours dans commandes créez un serveur avec la commande /create-server puis selectionnez PYTHON, accedez au panel et connectez vous avec vos identifiants.
Dans fichiers importer main.py, créer un ficher requirements.txt avec écrit "discord.py" dedans, allez dans "Startup" et mettez ca : 
Fichier de démarage : main.py
Modules de démarrage : discord.py
Vous pouvez dès maintenant allumer votre bot !
```
```
## ⚙️ Configuration

Modifiez les variables suivantes dans `main.py` :

```
ligne 54 : salon d'annonce des arrivents : channel = bot.get_channel(ID DU SALON)

ligne 59 et 60, récompenses pour les invitations? REMPLACER 5 PAR LE NOMBRE D'INVITATIONS Nésésésaires pour avoir le role :if invite_counts[inviter_id] == 5:
            role = member.guild.get_role(ID DU ROLE A DONNER)

ligne 73 : salon d'annonce des membre qui quitent votre serveur :  channel = bot.get_channel(ID DU SALON)

ligne 99, 100, 124 et 125 : pareil que la ligne 59 et 60 :     if invite_counts[member_id] >= 5 and (invite_counts[member_id] - amount) < 5:
        role = ctx.guild.get_role(ID DU ROLE )

dernière ligne : mettre votre token
```

## 📝 Commandes

### Commandes générales
- `!invites` : Voir son nombre d'invitations
- `!invites @user` : Voir le nombre d'invitations d'un utilisateur

### Commandes administratives
- `!give_invites @membre quantité` : Ajouter des invitations à un utilisateur
- `!suppr_invites @membre quantité` : Supprimer des invitations à un utilisateur

## 🔔 Notifications

Le bot envoie automatiquement des messages pour :
- Nouveaux membres rejoignant le serveur
- Membres quittant le serveur
- Attribution du rôle de récompense
- Modifications des invitations par les administrateurs

## 🛠️ Structure des données

Les données sont sauvegardées dans `invite_data.json` avec la structure suivante :
```json
{
    "user_id": nombre_invitations
}
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à contribuer !!

## 📜 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## 📫 Contact

Lucas_le_gamer (discord)
lucaslegamerpro@gmail.com

