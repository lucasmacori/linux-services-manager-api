# linux-services-manager-api

API des gestion des services linux.

Cet API permet d'effectuer les actions suivantes:
- Lister les services au statut 'enabled' sur linux
- Démarrer un service
- Stopper un service
- Ajouter, modifier ou supprimer des services favoris afin de les consulter plus rapidement

## 1. Installation

**Pré-requis**
- Python 3.7 ou supérieur
- Pip (souvent inclus avec python)
- Compilateur C++ (**Visual C++** sur windows, **GCC** sur linux par exemple)

**Installation des dépendances**

La commande suivante installe les dépendances depuis le fichier 'requirements.txt'

``` bash
python -m pip install -r requirements.txt
```

**Configuration**

Il est necéssaire de créer un fichier de configuration appelé **"config.json"**.
Le fichier se structure comme ceci:

``` json
{
    "port": 5000,
    "debug": true,
    "database": {
        "provider": "mysql",
        "host": "127.0.0.1",
        "user": "username",
        "password": "password",
        "database": "linuxservicesmanager"
    },
    "ssl": true,
    "cert": "linuxservicesmanager.crt",
    "key": "linuxservicesmanager.key"
}
```

**port**: Port que l'API va occuper, le port doit être disponible

**debug**: Si défini à **true**, la console affichera les opérations SQL effectuées

**database**.**provider**: Le type de base de données (mysql, postgres, oracle, cockroach)

**database**.**host**: L'adresse du serveur de base de données

**database**.**user**: L'utilisateur de la base de données

**database**.**password**: Le mot de passe de l'utilisateur de la base de données

**database**.**database**: Le nom de la base de données de l'API

**ssl**: Si défini à **true**, l'API sera consultable via le protocole HTTPS. Plutôt que HTTP

**cert**: Cette valeur est necéssaire si **ssl** est défini à **true**. Il s'agit du nom du fichier de certicat SSL

**key**: Cette valeur est necéssaire si **ssl** est défini à **true**. Il s'agit du nom du fichier de la clé SSL