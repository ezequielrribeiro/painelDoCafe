# painelDoCafe
Painel do café: um painel para a automatização da compra de cafés especiais em diferentes sites

## desenvolvimento

Trata-se de uma aplicação local, desenvolvida utilizando:
- textual: interface TUI (text user interface)
- selenium: motor para fazer o webscrapping nos sites

## sites suportados

o painel do café faz a coleta a partir dos sites:
- moka clube
- unique cafés
- netcafés

## funcionalidades

atualmente, o painel realiza:

- coleta de informações dos sites (a desenvolver)
- levantamento de preços e promoções (a desenvolver)
- levantamento de cupons de desconto (a desenvolver)

## comandos

permitir powershell executar scripts:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

instalar ambiente virtual:
```
python -m venv venv
source venv/bin/activate
```

ativar ambiente virtual:
```
.\venv\Scripts\activate
```

instalar dependências:
```
pip install -r requirements.txt
```
desativar ambiente virtual:
```
.\venv\Scripts\deactivate
```

executar script:
```
python main.py
```

