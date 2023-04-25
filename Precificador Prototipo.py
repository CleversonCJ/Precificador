import requests
import ast

# Pede ao usuário o valor do produto
while True:
    valor_produto_str = input('Digite o valor do produto: ')
    try:
        valor_produto = float(valor_produto_str)
        break
    except ValueError:
        print('Valor inválido! Por favor digite um valor numérico.')

# Pede ao usuário se existe algum custo extra
while True:
    cotacao_dolar_pref = input("Você quer adicionar a cotação do dólar ou usar a cotação do app? (Adicionar/App) ")

    if cotacao_dolar_pref == "Adicionar":
        # Pede ao usuário qual o valor extra
        while True:
            valor_dolar_str = input('Digite a cotação do dólar: ')
            try:
                cotacao_dolar = float(valor_dolar_str)
                break
            except ValueError:
                print('Valor inválido! Por favor digite um valor numérico.')
        break
    elif cotacao_dolar_pref == "App":
        # Faz a cotação do dólar comercial
        # URL da API do BCB
        url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados/ultimos/1?formato=json'

        # Faz a requisição à API
        response = requests.get(url)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Converte a resposta para um dicionário Python
            data = ast.literal_eval(response.text)

            # Extrai a cotação do dólar comercial
            cotacao_dolar_float = float(data[0]['valor'])
            cotacao_dolar = cotacao_dolar_float + (cotacao_dolar_float * 1.1 / 100 + cotacao_dolar_float * 2 / 100)
        else:
            print('Erro na solicitação HTTP.')
        break
    else:
        print('Resposta inválida! Por favor responda com "Adicionar" ou "App".')

# Converte o valor de dólar para real
valor_convertido = cotacao_dolar * valor_produto

# Atualiza o valor gasto
valor_atualizado = valor_convertido + (valor_convertido * 20 / 100)

# Pede ao usuário como ele prefere calcular a margem de lucro
while True:
    preferencia_margem_lucro = input("Como você prefere calcular a margem de lucro? (%/$) ")

    if preferencia_margem_lucro == "%":
        # Pede o valor em que o usuario quer como margem
        while True:
            margem_lucro_str = input('Digite o valor da margem de lucro: ')
            try:
                # Calcula a margem de lucro com referencia em porcentagem
                margem_lucro_porcentagem = float(margem_lucro_str)
                margem_lucro = valor_atualizado + (valor_atualizado * margem_lucro_porcentagem / 100)
                lucro_total = margem_lucro - valor_atualizado
                break
            except ValueError:
                print('Valor inválido! Por favor digite um valor numérico.')
        break
    elif preferencia_margem_lucro == "$":
        # Calcula o a margem de lucro com referencia em valor
        while True:
            margem_lucro_str = input('Digite o valor da margem de lucro: ')
            try:
                margem_lucro_valor = float(margem_lucro_str)
                margem_lucro = valor_atualizado + margem_lucro_valor
                lucro_total = margem_lucro - valor_atualizado
                break
            except ValueError:
                print('Valor inválido! Por favor digite um valor numérico.')
        break
    else:
        print('Resposta inválida! Por favor responda com "Sim" ou "Não".')

print(f'O custo do produto é R$ {valor_atualizado:.2f} \n O valor do lucro é: R$ {lucro_total:.2f} \n O valor final do produto é: R$ {margem_lucro:.2f}')
