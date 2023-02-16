# Quake Parser

## Tecnologias utilizadas
- Python 3.6


## Iniciando o projeto

### Instalando as dependências

É necessário primeiramente instalar as libs 
necessárias para executar o projeto,
para isso execute o seguinte comando em seu terminal:
```bash
$ pip install -i requirements.txt
```
São apenas libs utilizadas para criar a API do projeto


### Configurando o arquivo de inicialização

Existe um arquivo na pasta raiz do projeto chamado "**settings.ini**",
esse arquivo contém configurações do servidor como host e porta, como também
configurações do nome arquivo de entrada (o log) e o nome do arquivo de saída.

Sinta-se a vontade para modificar essas informações de acordo com a sua necessidade.


### Inicializando o projeto

Execute o seguinte comando em seu terminal na raiz do projeto:
```bash
$ python main.py
```

### Como utilizar o projeto?

A partir do host definido, você pode acessar a url (por padrão é: "0.0.0.0:8090")
e se tudo estiver correto você deverá receber a mensagem "Quake parser is running!"

A partir daí você pode utilizar os seguintes endpoints:
- [GET] **/matches**: Endpoint utilizado para retornar informações de todas as partidas do arquivo de log
- [GET] **/matches/{match_id}**: Endpoint utilizado para retornar informações de uma das partidas do arquivo de log

