from app import app, db

def testar_conexao():
    try:
        # Tenta executar uma consulta simples
        with app.app_context():
            resultado = db.session.execute("SELECT 1").fetchone()
            if resultado[0] == 1:
                print("✅ Conexão com o banco de dados estabelecida com sucesso!")
                print(f"URL do banco: {app.config['SQLALCHEMY_DATABASE_URI']}")
                return True
            else:
                print("❌ Falha na conexão com o banco de dados.")
                return False
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {str(e)}")
        return False

if __name__ == "__main__":
    testar_conexao()