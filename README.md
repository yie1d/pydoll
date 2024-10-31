<p align="center">
    <img src="https://github.com/user-attachments/assets/37b760b2-b13b-4a05-866c-0f8da739cbbd" alt="Alt text" />
</p>
<br>

PyDoll é uma biblioteca pensada em automatizar navegadores baseados no Chromium sem a necessidade de webdriver e com interações mais realísticas. Feita inspirada no Selenium e Puppeteer, tem suporte total a assincronidade do Python, o que permite um desempenho melhor, além de possibilidades como captura de eventos.

# TODO List

- [ ] Implementar sistema de portas randômicas, para possibilitar
abertura de vários browsers.
- [ ] Criar exceptions personalizadas.
- [ ] Adicionar sistema para verificar se o clique foi realizado 
com sucesso.
- [ ] Melhorar sistema de conexão com o protocolo, monitorando de forma
mais ativa.
- [ ] Mapear eventos para `Page`, `Browser`, `Network`, etc.
- [ ] Implementar sistema de proxy.
- [ ] Criar uma pasta temporária para o AppData do navegador.
- [ ] Substituir leitura e escrita de arquivos por uma biblioteca async.
- [ ] Melhorar documentação.
- [ ] Adicionar funcionalidade de clique com posição randômica.
- [ ] Implementar padrão Singleton para a classe `ConnectionHandler`.
- [ ] Fazer melhoria no sistema de atributos de `WebElement`:

```python
class WebElement:
    def __init__(self, node: dict, connection_handler: ConnectionHandler):
        self._node = node
        self._connection_handler = connection_handler
        self._attributes = {}

    # cria properties para atributos mais comuns
    @property
    def class_name(self):
        return self._attributes.get('class_name')

    @property
    def id(self):
        return self._attributes.get('id')
    
    # método para obter atributos mais específicos
    def get_attribute(self, key: str):
        return self._attributes.get(key)
```

- [ ] Testes automatizados.
- [ ] Integração contínua para verificar formatação do código.
