
# Sistema de Estabelecimentos

Este é um projeto desenvolvido com **Flask** para gerenciamento de estabelecimentos. Ele permite a criação, leitura, atualização e exclusão de estabelecimentos cadastrados, com funcionalidades para cálculo de proximidade entre os estabelecimentos.

## Funcionalidades

- **Cadastro de Estabelecimentos**: Adicionar novos estabelecimentos com nome, latitude e longitude.
- **Listagem de Estabelecimentos**: Exibir todos os estabelecimentos cadastrados em uma tabela.
- **Edição de Estabelecimentos**: Alterar os dados de um estabelecimento (nome, latitude e longitude).
- **Exclusão de Estabelecimentos**: Remover um estabelecimento após confirmação do usuário.
- **Relatórios**:
  - Estabelecimentos dentro de um raio de 5km de um nome informado.
  - Estabelecimentos mais próximos a um ponto geográfico específico.
  - Estabelecimentos dentro de um raio de 10km.

## Tecnologias Utilizadas

- **Flask**: Framework web em Python.
- **MongoDB**: Banco de dados NoSQL para armazenamento dos estabelecimentos.
- **Geopy**: Biblioteca para cálculos de distância geográfica.
- **SweetAlert2**: Biblioteca para alertas bonitos no frontend.
- **HTML/CSS**: Para a construção da interface gráfica.

## Instalação

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
ou 
python3 -m venv venv

source venv/bin/activate  # no Windows, use venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Execute a aplicação:

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

## Como Usar

1. **Cadastrar Estabelecimentos**: Vá para a página de cadastro (`/cadastrar-form`), insira o nome, latitude e longitude, e clique em "Cadastrar".
2. **Listar Estabelecimentos**: Acesse a página de listagem (`/listar-todos`) para visualizar todos os estabelecimentos cadastrados.
3. **Editar Estabelecimentos**: Clique em "Editar" na tabela para modificar os dados de um estabelecimento.
4. **Excluir Estabelecimentos**: Clique em "Excluir" e confirme a exclusão do estabelecimento com o alert.
5. **Relatórios**: Acesse as páginas de relatórios para consultar os estabelecimentos dentro de um raio de 5km, 10km ou mais próximos a um ponto específico.
