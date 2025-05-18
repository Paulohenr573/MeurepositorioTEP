Aula 3 - 11-03-2025

# 🎤 Aplicativo Karaokê com Python e API GROQ

## Descrição
Este projeto consiste na criação de um aplicativo funcional utilizando Python e a API da GROQ. O objetivo é possibilitar o upload de arquivos MP3, oferecendo uma interface intuitiva de controle da reprodução (início, pausa e parada) e realizar a transcrição da letra da música, criando uma tela estilo karaokê para que o usuário possa acompanhar a letra em tempo real.

## Ferramentas Utilizadas
### Ambiente de Desenvolvimento
- **Visual Studio Code** – Editor de código utilizado no projeto.
- **Python** – Linguagem de programação principal.

### APIs e Tecnologias
- **GROQ API** – Usada para processar a transcrição da música.

## Funcionalidades
- Upload de arquivos MP3.
- Reprodução de música com controles intuitivos.
- Transcrição da letra da música.
- Tela de karaokê (em desenvolvimento).

## Desafios e Aprendizados
A interface de controle foi bem implementada, porém o principal desafio foi sincronizar a exibição da letra com a música. Algumas estratégias exploradas incluíram ajustes na captura de tempo e sincronização com a IA, mas ainda não obtive um resultado satisfatório. Futuramente, pretendo testar outras abordagens para esse problema.

## Como Executar
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute o aplicativo: `python app.py`
3. Faça upload de um arquivo MP3 e utilize os controles para reprodução.

## Próximos Passos
- Melhorar o design da interface.
- Aperfeiçoar a sincronização da letra na tela de karaokê.
- Explorar outras APIs para melhorar a transcrição.

---