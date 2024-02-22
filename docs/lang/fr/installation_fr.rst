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

