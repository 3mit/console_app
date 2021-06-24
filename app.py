import click
import requests
from dotenv import load_dotenv, dotenv_values

config = dotenv_values(".env")
load_dotenv()

class Pokemon():
    _id: str  
    identify: int
    name: str
    base_experience: int
    height: int
    is_default: bool
    order: int
    weight: int
    __v: int

class Trainer():
    _id:str  
    name: str
    pokemons: list

@click.group()
def commands():
    pass

@commands.command('capture')
@click.option('--find', default='')
def capture_pokemon(find: str):
    if(find is ''):
        print('Debe ingresar el nombre o el indentificador del pokemon a capturar')
        return

    try:
        name_trainer: str = click.prompt('Ingrese su nombre de entrenador', type=str)
    except:
        print('Debe ingresar su nombre de entrenador')
        return

    exit_program = False    
    pokemons = []

    while(exit_program != True):

        response = requests.get(config.get('API_URL') + 'pokemon/' + find) 
        pokemon: Pokemon = response.json()

        if(pokemon is not None):

            options: str = click.prompt('Desea capturar a ' + pokemon['name'] + "? (si/no/salir)", type=str)

            if(options == 'si'):
                pokemons.append(pokemon['_id'])
                data = {
	                'name': name_trainer,
	                "pokemons": pokemons
                }
                print(str(data)[1:-1] )
                rs = requests.post(config.get('API_URL') + 'trainer', data)

                if(rs.status_code == 201):
                    print('A capturado a ' + pokemon['name'])
                else:
                    print('No se a logrado guardar su solicitud')

                find: str = click.prompt('Ingrese el nombre o indentificador del pokemon a buscar', type=str)

            elif(options == 'salir'):
                exit_program = True
            else:
                find: str = click.prompt('Ingrese el nombre o indentificador del pokemon a buscar', type=str)
       

@commands.command('trainer')
@click.option('--name', default='')
def view_pokemnon(name: str):

    if(name is ''):
        print('Debe ingresar el nombre del entrenador a buscar')
        return

    response = requests.get(config.get('API_URL') + 'trainer/' + name) 
    trainer: Trainer = response.json()
    if(response.status_code == 200):
        print('Nombre Entrenador:' + trainer['name'])
        print('\nPokemones ')
        for x in trainer['pokemons']:
            print('\nID:' + x['_id']) 
            print('nombre:' + x['name']) 
            print('Experiencia base:' + str(x['base_experience'])) 
            print('Identificacion:' + str(x['identify'])) 
            print('Altura:' + str(x['height'])) 
            print('Por Defecto:' + str(x['is_default']))
            print('Orden:' + str(x['order']))
            print('Peso:' + str(x['weight']) + "\n") 
    else:
        print('No se a encontrado el entrenador solicitado')

    

@commands.command('free')
@click.option('--name', default='')
def view_pokemnon(name: str):

    if(name is ''):
        print('Debe ingresar el nombre del entrenador a buscar')
        return

    response = requests.get(config.get('API_URL') + 'trainer/' + name) 
    trainer: Trainer = response.json()

    pokemons = []

    if(response.status_code == 200):

        print('Cual de los pokemones desea liberar? <ingrese el id>\n')
        print('Pokemones ')

        for x in trainer['pokemons']:
            pokemons.append(x['_id'])
            print('\nID:' + x['_id']) 
            print('nombre:' + x['name']) 

        id: str = click.prompt('\nIngrese el indentificador del pokemon a liberar', type=str)

        for index, x in enumerate(trainer['pokemons']):
            if(x['_id'] == id):
                pokemons.pop(index)

        data = {
	        'name': trainer['name'],
	        "pokemons": pokemons
        }

        response = requests.put(config.get('API_URL') + 'trainer/' + trainer['_id'], data) 

        if(response.status_code == 200):
            print('Se a liberado el pokemon solicitado')
        else:
            print('No se a logrado guardar su solicitud')

    else:
        print('No se a encontrado el entrenador solicitado')


cli = click.CommandCollection(sources=[commands])

if __name__ == '__main__':
    cli()
