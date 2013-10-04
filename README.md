Torta da Sieve
=====

Precisamos criar uma API que fornecerá dados da nossa base. 
Essa API será necessária para criarmos uma tela que exibirá relatórios dos produtos de um cliente.

Como começar?
--------------------
Faça um fork desse projeto base, ele já possui os modelos que você precisa, deixando para você apenas a implementação da view e da API. Avaliaremos tudo que for feito, mesmo que o código não contemple todas as features pedidas.
> "Definido por você o prazo será."


Critérios de Avaliação
--------------------
Os seguintes aspectos do seu projeto serão avaliados, além de quão longe você prosseguiu no caminho da força:

* Agilidade;
* Legibilidade;
* Escopo;
* Organização do código;
* Padrões de projeto;
* Existência e quantidade de bugs e gambiarras;
* Cobertura da aplicação com testes;


Primeiro passo - API
--------------------
A API que será criada deverá ser capaz de receber requisições *GET*, *POST*, *PUT* e *DELETE*, permitindo assim que as operações CRUD possam ser realizadas no seu produto. 

Segue abaixo um exemplo de uma resposta de uma requisição *GET*:

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


Segundo passo - Interface de visualização
--------------------

Agora precisamos exibir esses dados para o nosso cliente, além de permitir as operações de criação, edição e deleção de seus produtos. Vale usar Javascript e qualquer um de seus plugins, mas não exagere. Use a força e crie o conceito de como os dados são exibidos, formatados, etc.

Terceiro passo - Performance Jedi (BÔNUS)
--------------------

Conseguir trazer os dados requisitados em apenas uma query.


![Patience, young Padawan](http://melindascollins.com/wp-content/uploads/2013/04/patience-yoda.jpg)
