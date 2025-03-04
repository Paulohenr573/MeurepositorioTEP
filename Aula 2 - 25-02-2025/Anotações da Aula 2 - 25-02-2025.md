Anotações da Aula 2 - 25-02-2025

- Tema da aula: Criação de um chatbot no terminal utilizando Python e API da OpenAI.
- Ferramentas utilizadas:
  - Python
  - VS Code
  - Biblioteca openai
- Atividade desenvolvida:
  - Gerar uma chave de API da OpenAI: `[SUA-CHAVE-AQUI]`.
  - Desenvolver um chatbot básico no terminal para receber e processar mensagens usando a API.
- Passos principais:
  1. Configurar ambiente virtual com .venv.
  2. Escrever o código do chatbot: from openai import OpenAI
client= OpenAI()

completion = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Você é uma vendedora de pastel eficiente."},
        {"role": "user", "content": "Me indique os melhores pasteis para hoje com bacon!"}
    ]
)

print(completion.choices[0].message).
- Aprendizados:
  - Uso de APIs para integração com IA.
  - Configuração de ambiente virtual para isolamento de dependências.
  - Operação do chatbot no terminal.

- Desafios enfrentados:
  - A instalação e validação da chave no terminal foi mais complicada do que parecia inicialmente. Qualquer letra faltante ou trocada gerava várias linhas de erro no terminal, o que dificultou bastante o progresso. Com a ajuda do professor, conseguimos identificar as falhas e seguir adiante.


- Observações finais:
  - O uso da API da OpenAI mostrou diversas possibilidades interessantes para projetos futuros, especialmente na criação de chatbots personalizados.
  - Foi interessante aprender sobre o "controle de temperatura", que permite ajustar o tom das respostas do chatbot. Essa funcionalidade abre margem para adaptações criativas no comportamento da IA.

