import logging
import sys

def setup_logging():
    """Configura el logging para toda la aplicación."""
    
    # Formato del log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración básica
    logging.basicConfig(
        level=logging.INFO,  # Nivel global
        format=log_format,
        handlers=[
            # Console output
            logging.StreamHandler(sys.stdout),
            # File output
            logging.FileHandler("app.log", encoding="utf-8")
        ]
    )
    
    # Configurar niveles específicos por módulo
    logging.getLogger("src.rag.retriever").setLevel(logging.DEBUG)
    logging.getLogger("langchain").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.ERROR)

if __name__ == "__main__":
    setup_logging()