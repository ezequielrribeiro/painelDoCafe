# painelDoCafe
Painel do café: um painel para a automatização da compra de cafés especiais em diferentes sites

## desenvolvimento

Trata-se de uma aplicação local, desenvolvida utilizando:
- textual: interface TUI (text user interface)
- selenium: motor para fazer o webscrapping nos sites

## sites suportados

o painel do café faz a coleta a partir dos sites:
- Moka Clube (produtos)
- Unique Cafés (produtos)
- Netcafés (produtos)
- Café Dutra (promoções e produtos)
- Encantos do Café (promoções e produtos)

## funcionalidades

atualmente, o painel realiza:

- levantamento de preços e promoções (a desenvolver)
- coleta de produtos de cada site (a desenvolver)

## comandos

permitir powershell executar scripts:
```
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
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
py main.py
```