"""Application factory per RAGlite."""

from __future__ import annotations

import os

from flask import Flask

from . import db

RAG_CHUNK_SIZE=110
RAG_CHUNK_OVERLAP=1

def create_app(test_config: dict | None = None) -> Flask:
    """Crea e configura l'istanza Flask.

    Args:
        test_config: dizionario di configurazione usato nei test
                     per sovrascrivere i valori di default.
                     Se None, viene caricato instance/config.py (se esiste).
    """
    app = Flask(__name__, instance_relative_config=True)  # TODO: True o False? Perché?

    app.config.from_mapping(
        SECRET_KEY="dev",  # TODO: setta la key per lo sviluppo locale?
        DATABASE=os.path.join(app.instance_path, "raglite.sqlite"),  # TODO: leggi da app il path giusto
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)  # TODO: specifica il file di config; perché silent=True?
    else:
        app.config.from_mapping(test_config)  # TODO: il dizionario test_config?

    os.makedirs(app.instance_path, exist_ok=True)  # TODO: usa l'attributo di app con il path di instance/
    print(app.instance_path)
    from . import rag
    app.register_blueprint(rag.bp)  # TODO: registra il blueprint?

    db.init_app(app)
    
    return app