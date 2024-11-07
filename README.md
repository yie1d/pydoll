<p align="center">
    <img src="https://github.com/user-attachments/assets/37b760b2-b13b-4a05-866c-0f8da739cbbd" alt="Alt text" />
</p>
<br>

PyDoll é uma biblioteca pensada em automatizar navegadores baseados no Chromium sem a necessidade de webdriver e com interações mais realísticas. Feita inspirada no Selenium e Puppeteer, tem suporte total a assincronidade do Python, o que permite um desempenho melhor, além de possibilidades como captura de eventos e webscrapping simultâneo.

# TODO List

- [x] Implementar sistema de portas randômicas, para possibilitar
abertura de vários browsers.
- [x] Criar exceptions personalizadas.
- [x] Melhorar sistema de conexão com o protocolo, monitorando de forma
mais ativa.
- [x] Mapear eventos para `Page`, `Browser`, `Network`, etc.
- [x] Implementar sistema de proxy.
- [x] Criar uma pasta temporária para o AppData do navegador.
- [x] Substituir leitura e escrita de arquivos por uma biblioteca async.
- [x] Adicionar funcionalidade de clique com offset.
- [x] Fazer melhoria no sistema de atributos de `WebElement`:
- [x] Criar uma classe chamada Page e separar da classe Browser. Assim, podemos lidar com múltiplas abas em simultâneo.
- [ ] Adicionar sistema para verificar se o clique foi realizado 
com sucesso.
- [ ] Criar gerador de fingerprint
- [ ] Criar classe Keyboard, para simular teclado.
- [ ] Melhorar documentação.
- [ ] Testes automatizados.
- [ ] Integração contínua para verificar formatação do código.
