Flask-Firewall
==============
Permet une gestion d'un firewall pour l'accès aux ressources/pages de votre application sous Flask.

L'autorisation d'une page ou le refus d'une page dépend de la gestion d'un ou plusieur "groupe" valide.

Utilisation
===========

Flask-exemple.py
----------------
Il suffit de prendre le dossier **security** du repository github et de l'insérer dans votre applicarion sous Flask.

Dans votre application Flask, il serai judicieux d'éxécuter ce "hook" avant que la requête soit complètement gerée.
Nous utilisons ici le décorateur *@app.before_request*.

Vous trouverez un exemple fonctionnel dans ce repository; **flask-example.py**

```python
  @app.before_request
  def pre_request():
  
      # here get my user, get group for this user
      
      user_groups = ["IS_ADMIN"] # le groupe de notre user, une liste de groupe qu'il fait parti est possible
      # magic start here, si utilisateur fait parti d'un groupe non autorisé -> error 403
      flask_firewall(request, user_groups, abort)
```

Configutation
-------------
Le fichier de configuration du firewall se trouve dans **security/firewall/flask_firewall.json**

Vous pouvez dans ce fichier de configuration spécifique pour chaque (pattern) route quel groupe y accède.

Les routes qui sont incluse dans le test ainsi que les routes qui ne le sont pas.

Voici un exemple de fichier de configuration (avec quelque commentaire).

```json
{
  "flask_firewall":
  {
    "author": "Ruiz Sanchez Carlos",
    "version": "v1.0",
    "github": "https://github.com/cruizsan/Flask-Firewall",
    "routing": # ici que vous devez ajouter/supprimer des configurations de routes
    {
      "include": # les routes qui sont incluse dans les tests du firewall
      [
        {
          "route": "^/api/*", # toute les routes qui ont le format /api/xxxx seront testée
          "groups": ["IS_USER", "IS_ADMIN"], # si utilisateur fait parti du groupe IS_USER ou IS_ADMIN, il peux acceder à  cette route
          "error_code": 403 # si il y'a erreur, le code qui sera lancée (== si pas un groupe correct pour cette route)
        },
        {
          "route": "^/anonym/*", # toute les routes qui ont le format /anonym/xxxx seront testÃ©e
          "groups": ["IS_ANONYMOUS"], # si utilisateur fait parti du groupe IS_ANONYMOUS, il peux acceder à  cette route
          "error_code": 400 # si il y'a erreur, le code qui sera lancée
        }
      ],
      "exclude": ["^/static/*"] # cette route ne sera pas testée par le firewall (libre d'accès)
    }
  },
  "behavior": "unauthorized" # quel comportement faire pour les routes non matchée (non existante dans le firewall)
                                > unauthorized : seront limitée (403)
                                > authorized : seront libre d'accès
}
```

TIPS
----

    * Vous pouvez gérer vous même quel rendu/fonction à éxécuter via le gestion d'erreur de Flask
        * Custom error pages(Flask) : http://flask.pocoo.org/docs/0.11/patterns/errorpages/
    
    * Attention à l'ordre dans la création des règles de routing de firewall
        * Les test s'arrête au premier qu'il match (faire des règles les plus restrictive au moins restrictive)
