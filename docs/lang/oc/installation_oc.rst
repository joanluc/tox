Installacion
============ 

per pipx 
-------- 

:pypi:'tox' es un esplech CLI qu'a besonh d'un interpréteur Python (version 3.7 o superiora) per foncionar. 
Recomandam :pypi:'pipx' per Installatz tox dins un environament isolat. 
Aquò presenta l'avantatge suplementari que mai tard, poiretz metre a nivèl tox sens afectar d'autras partidas del sistèma.

.. code-block:: bash

    python -m pip install pipx-in-pipx --user
    pipx install tox
    tox --help

per pip 
------- 

Alternativament, lo podètz installar dins l'interpréteur Python global el meteis (benlèu coma paquet utilizator pel fichièr ''--usar''). 
Siatz prudent s'utilizatz una installacion Python gerida per vòstre sistèma d'espleitacion o un autre gestionari de paquets. 
''pip'' se pòt coordinar pas amb aqueles espleches, e pòt daissar vòstre sistèma dins una situacion incoerenta. estat. 
Notatz que se manlevatz aquela via, vos devètz assegurar que pip es pro recent confòrmament als jos-seccions çai jos :

.. code-block:: bash

    python -m pip install --user tox
    python -m tox --help
