from alembic import context
from sqlalchemy import engine_from_config, pool, MetaData
from logging.config import fileConfig
from api import create_app, db  # Importe db se você estiver usando Flask-SQLAlchemy

# Configuração do arquivo de log para Alembic
config = context.config
fileConfig(config.config_file_name)

# Definição dos metadados alvo (substitua com seus próprios metadados)
target_metadata = db.metadata  # Substitua 'db.metadata' com seus próprios metadados

# Função para executar migrações no modo offline
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# Função para executar migrações no modo online
def run_migrations_online():
    app = create_app()  # Crie o aplicativo Flask
    with app.app_context():
        # Configure a engine usando as configurações do Flask
        connectable = engine_from_config(
            app.config,
            prefix='sqlalchemy.',
            poolclass=pool.NullPool
        )

        # Configure o contexto do Alembic para utilizar a conexão da engine
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
            )

            # Execute as migrações dentro de uma transação
            with context.begin_transaction():
                context.run_migrations()

# Verifica se estamos no modo offline ou online e executa as migrações correspondentes
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()