import json
import requests as rq
from flask import Flask, request, render_template

app = Flask(__name__)
app.run(debug=True)

# Chave gerada no site : http://api.openweathermap.org  para a busca na API
api_key = 'eb7daf8b6d9a3607541965d82a76ad80'

# @app.route se refere a rota utilizada, o caminho que o usuario precisa ir para executar determinada função dentro de uma API
# @app.route também pode conter um segundo parametro chamado "methods", deve-se passar uma lista de métodos HTTP Restful (POST, GET, PUT , DELETE, HEAD e etc...) para serem executando sob uma mesma rota.

# ------------------ [DESCRIÇÃO DE MÉTODOS] ---------------------------------------------------------------------
# POST -> Deve-se usar POST quando é desejado inserir dados no banco de dados por exemplo, ou fazer um Login.
# GET -> Recuperar dados do servidor. Exemplos uma busca ou listagem de pessoas de uma determinada disciplina por exemplo
# DELETE -> Deleta os dados
# PUT -> Usado para atualização de dados. 


#       render_template é uma função usada para renderizar um arquivo html, ele aceita outro parametro opcional "data", iguale as informações que quer mandar para a pagina HTML usando data=dados ou data=seja_la_o_que_for
#       request é uma biblioteca do flask para lidar com dados que vem de pedidos dos clientes, algumas coisas uteis que essa biblioteca é capaz de fazer é te dizer qual método foi utilizado na requisição

#       request.args.get() pega requisições que são feitas atraves da URL, aquelas no formato http://localhost:5000/algumaPagina.html?nome=CursoFlaskAPI  tudo que vem depois de '?' pode ser acessado por esse metodo
# nesse caso basta usar um dos argumentos passado na URL, nesse caso usamos 'nome' então fariamos algo como request.args.get('nome') , isso deve retornar 'CursoFlaskAPI'

#       request.json() pega uma requisição que veio atráves de uma requisição JSON
#       request.form pega dados que vieram através do formulario, mas não vieram pela URL. Uma típica cena de uso do método POST.

#       A biblioteca requests, que é do python ela serve para fazer chamadas a páginas. 
#               requests.get() usa o método GET
#               requests.post() usa o método POST
#               requests.put() usa o método PUT
#               requests.delete() usa o método PUT

#       Link para mais detalhes :  https://www.w3schools.com/python/module_requests.asp

#       json é uma biblioteca python para o uso eficientes de objetos JSON 

#       Link para mais detalhes : https://www.w3schools.com/python/python_json.asp




@app.route('/')
def weather_page():
    return render_template('weather.html')

@app.route('/data/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'GET': 
        city = request.args.get('cidade')

        # Faço uma requisição para a API de clima. Usando o nome da cidade passado na busca e a chave gerada pela API para o acesso. 
        weather_response = rq.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}') 

        # O resultado de weather_response é do tipo Response, logo não posso convetê-lo para JSON, mas o objeto Response tem uma propriedade que se chama 'text' que retorna a Response em String.
        # Usamos então json.loads para carregar essa string em um objeto JSON 
        weather_json_data = json.loads(weather_response.text)

        
        # Aqui estamos sobrescrevendo os valores de temp, temp_min, temp_max, feels_like pelo convertido das termperaturas que são em kelvin para celcius
        weather_json_data['main']['temp'] = kelvinToCelcius( weather_json_data['main']['temp'] )
        weather_json_data['main']['temp_min'] = kelvinToCelcius( weather_json_data['main']['temp_min'] )
        weather_json_data['main']['temp_max'] = kelvinToCelcius( weather_json_data['main']['temp_max'] )
        weather_json_data['main']['feels_like'] = kelvinToCelcius( weather_json_data['main']['feels_like'] )



        return render_template('weather_info.html', data=weather_json_data)


# Essa função é responsável por receber uma temperatura em graus kelvin e retornar o valor correspondente em celcius.
# a função round, arrendonda o número quebrado em quantas casas decimais queira, nesse caso queremos apenas 2 casas decimais depois da virgula. Então algo como 25,392938 °C se torna 25,39 °C

def kelvinToCelcius(temp):
    celcius = (temp - 273.15)
    return round(celcius,2)