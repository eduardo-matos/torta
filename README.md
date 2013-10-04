Torta da Sieve
=====

Precisamos criar uma API que se alimentará dos dados da nossa base. 
Essa API será necessária para criarmos uma tela que exibirá relatórios dos produtos de um cliente.

Como começar?
--------------------
Faça um fork desse projeto base, ele já possui os modelos que você precisa, deixando para você apenas a implementação da view e da API. Assim que terminar, nos sinalize de alguma forma. =)


Critérios de Avaliação
--------------------
Os seguintes aspectos do seu projeto serão avaliados, além de quão longe você prosseguiu no caminho da força:

* Legibilidade;
* Organização do código;
* Padrões de projeto;
* Cobertura da aplicação com testes;


Primeiro passo - API
--------------------

Uma requisição deve ser feita e ela deverá retornar um JSON no seguinte formato:


```
{
    'produtos': [
    {
        'nome': 'Torta de limao',
        'meu_preco': '9.99',
        'disponibilidade': true,
        'codigo':1,
        'urls': [{
            'endereco': 'meuconcorrente.com.br/tortalimao',
            'preco': '10.0'
        }, 
        {
            'endereco': 'meuoutroconcorrente.com.br/tortalimao',
            'preco': '10.1'
        }
    },
  
    {
      'nome': 'Torta alema',
      'meu_preco': '9.99',
      'disponibilidade': true,
      'codigo':1,
      'urls': [{
            'endereco': 'meuconcorrente.com.br/tortaalema',
            'preco': '10.5'
        }
    }]
}
```


Segundo passo - Exibição dos dados
--------------------

Agora precisamos exibir esses dados para o nosso cliente. Vale usar Javascript e qualquer um de seus plugins, mas não exagere. Use a força e crie o conceito de como os dados são exibidos, formatados, etc.

Terceiro passo - Performance Jedi (BÔNUS)
--------------------

Conseguir trazer os dados requisitados em apenas uma query.


![Patience, young Padawan](http://melindascollins.com/wp-content/uploads/2013/04/patience-yoda.jpg)
