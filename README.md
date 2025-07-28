# Projeto Trees Everywhere

## Em construção

### Descrição

O projeto **Trees Everywhere** foi criado para o desafio da vaga de desenvolvedor backend júnior.

O objetivo principal do projeto é manter um banco de dados de árvores plantadas por voluntários espalhados pelo mundo. Usuários podem estar associados a uma ou mais contas, permitindo que vejam as árvores plantadas pelo grupo de usuários da mesma conta.

---

## Funcionalidades implementadas

### Páginas de Admin

- Cadastro de novos usuários e senha, com possibilidade de associar cada usuário a uma conta.
- Listagem e criação de contas (modelo `Account`).
- Ativação e desativação de contas diretamente na tela de listagem.
- Cadastro e visualização de plantas (modelo `Plant`).
- Visualização detalhada de uma planta, incluindo a lista de todas as árvores daquele tipo plantadas, mostrando também o nome da pessoa que plantou.

### Template Views

- Login de usuários cadastrados pelo admin.
- Visualização das árvores plantadas por um usuário, garantindo que um usuário não possa visualizar as árvores plantadas por outro usuário.
- Exibição dos dados de uma árvore plantada específica.
- Adição de uma nova árvore plantada.
- Exibição de todas as árvores plantadas nas contas das quais o usuário é membro.

### API REST

- Método que retorna, em formato JSON, a lista de todas as árvores plantadas pelo usuário atualmente logado.

### Testes automatizados

- Cenário de teste com duas contas, três usuários distribuídos entre as contas e árvores plantadas por cada um.
- Teste de template para garantir que a listagem de árvores plantadas por um usuário específico está sendo renderizada corretamente.
- Teste de template que verifica se tentar acessar as árvores plantadas por outro usuário retorna erro 403 (Forbidden).
- Teste de template para validar a listagem de árvores plantadas pelos usuários das contas às quais o usuário pertence.
- Testes unitários para os métodos `User.plant_tree()` e `User.plant_trees()`, demonstrando que os objetos `PlantedTree` são criados e associados corretamente ao usuário.

---

## Tecnologias e ferramentas extras adicionadas

- Estilização dos templates HTML utilizando Tailwind CSS para uma interface limpa, responsiva e moderna.
- Integração do Swagger para documentação API REST.

---

## Como usar o Swagger para testar a API

1. O Swagger está disponível na rota:

http://127.0.0.1:8000/swagger/

2. Para autenticar e poder testar as rotas protegidas da API, primeiro gere o token de autenticação usando a rota:

http://127.0.0.1:8000/api-token-auth/?username=SEU_USUARIO&password=SUA_SENHA

Exemplo:

http://127.0.0.1:8000/api-token-auth/?username=teste&password=123456789mmm

Essa rota retorna um JSON com o token, por exemplo:

{
"token": "abc123def456..."
}

3. Copie o token retornado.

4. No Swagger, clique no botão **Authorize** no topo da página e informe o token no formato:

Token abc123def456...

5. Agora você pode testar as rotas protegidas da API usando o Swagger com o token autenticado.

---

Se preferir, você também pode passar o token diretamente no cabeçalho `Authorization` nas requisições para a API, usando o formato:

Authorization: Token abc123def456...

---

## Como rodar o projeto localmente

### 1. Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd trees_everywhere
```

### 2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados (por padrão SQLite):

### 5. Execute as migrações para criar as tabelas no banco de dados:

```bash
python manage.py migrate
```

### 6. Crie um superusuário para acessar o admin:

```bash
python manage.py createsuperuser
```

### 7. Execute o servidor de desenvolvimento:

```bash
python manage.py runserver
```

## 8. Acesse no navegador:

### Admin: http://127.0.0.1:8000/admin/

### Aplicação: http://127.0.0.1:8000/

### 9. Para rodar os testes automatizados:

```bash
python manage.py test
```
