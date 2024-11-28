# Projeto: Gerador de quiz

Esse é um projeto da matéria "Padrões de Projeto e Frameworks", para a tarefa <a href="https://ava.ifpr.edu.br/mod/assign/view.php?id=393948">Gerador de quiz - parte 1</a>.

## Padrões utilizados

A seguir, uma enumeração dos padrões que foram utilizados no projeto, seu propósito, e onde no código foi utilizado.

### Singleton

O Singleton é um padrão de projeto que garante que uma classe tenha apenas uma instância e fornece um ponto de acesso global a ela, através de um método implementado na classe que retorna a instancia.

O padrão Singleton foi utilizado no arquivo "/main.py" na classe "App", para que exista sempre apenas uma classe App.

### Facade

O padrão Facade é um padrão de projeto estrutural que fornece uma interface simplificada para um subsistema complexo, ocultando os detalhes internos e reduzindo o acoplamento entre os componentes.

O padrão Facade foi utilizado no arquivo "/main.py na classe "App", para reduzir a inicialização de um quiz (Exame e correção) a um único método.

### Template Method

O padrão Template Method é um padrão de projeto comportamental que define o esqueleto de um algoritmo, delegando algumas etapas para subclasses. Ele permite que subclasses implementem partes específicas do algoritmo sem alterar sua estrutura geral.

O padrão Template foi utilizado no arquivo "/models/exam.py" na classe "Exam", para encapsular as diferentes formas de se pontuar e mostrar a pontuação de um quiz. Os templates estão definidos na pasta "/templates".