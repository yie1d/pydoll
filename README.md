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
- [ ] Adicionar factory para `WebElement`, criando subclasses, por exemplo:

```python
class ElementFactory:
    @staticmethod
    def create_element(node: dict, connection_handler: ConnectionHandler) -> WebElement:

        if node['nodeName'] == 'BUTTON':
            return ButtonElement(node, connection_handler)
        elif node['nodeName'] == 'INPUT':
            return InputElement(node, connection_handler)
        else:
            return WebElement(node, connection_handler)

class ButtonElement(WebElement):
    def click(self):
        print("Clicking the button")

class InputElement(WebElement):
    def send_keys(self, text: str):
        print("Sending keys to input")
```

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
