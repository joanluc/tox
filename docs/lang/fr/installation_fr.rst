Installation
============ 

via pipx 
-------- 

:pypi:'tox' est un outil CLI qui a besoin d'un interpréteur Python (version 3.7 ou supérieure) pour fonctionner. 
Nous recommandons :pypi:'pipx' pour Installez tox dans un environnement isolé. 
Cela présente l'avantage supplémentaire que plus tard, vous pourrez mettre à niveau tox sans affecter d'autres parties du système.

.. code-block:: bash

    python -m pip install pipx-in-pipx --user
    pipx install tox
    tox --help

via pip 
------- 

Alternativement, vous pouvez l'installer dans l'interpréteur Python global lui-même (peut-être en tant que paquet utilisateur via le fichier ''--user''). 
Soyez prudent si vous utilisez une installation Python gérée par votre système d'exploitation ou un autre gestionnaire de paquets. 
''pip'' peut ne pas se coordonner avec ces outils, et peut laisser votre système dans une situation incohérente. état. 
Notez que si vous empruntez cette voie, vous devez vous assurer que pip est suffisamment récent conformément aux sous-sections ci-dessous :

.. code-block:: bash

    python -m pip install --user tox
    python -m tox --help
