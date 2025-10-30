# Trabalhando com IFrames

IFrames (inline frames) são um dos aspectos mais complicados da automação de navegadores. O Pydoll fornece uma API limpa e intuitiva para interação com iframes que abstrai a complexidade do gerenciamento de alvos (targets) do CDP.

## Guia Rápido

### Interação Básica com IFrame

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def interact_with_iframe():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com/page-with-iframe')
        
        # Encontre o elemento iframe
        iframe_element = await tab.find(tag_name='iframe', id='content-frame')
        
        # Obtenha uma instância de Tab para o iframe
        iframe = await tab.get_frame(iframe_element)
        
        # Agora interaja com elementos dentro do iframe
        button = await iframe.find(id='submit-button')
        await button.click()
        
        # Encontre e preencha o formulário dentro do iframe
        username = await iframe.find(name='username')
        await username.type_text('john_doe')

asyncio.run(interact_with_iframe())
```

!!! tip "IFrames são Apenas Abas (Tabs)"
    No Pydoll, um iframe retorna um objeto `Tab`. Isso significa que **todos os métodos disponíveis em Tab funcionam em iframes**: `find()`, `query()`, `execute_script()`, `take_screenshot()`, e mais.

## Entendendo IFrames

### O que é um IFrame?

Um `<iframe>` (inline frame) é um elemento HTML que incorpora outro documento HTML dentro da página atual. Pense nisso como uma "janela do navegador dentro de outra janela do navegador".

```html
<html>
  <body>
    <h1>Página Principal</h1>
    <p>Este é o documento principal</p>
    
    <iframe src="https://other-site.com/content.html" id="my-frame">
    </iframe>
  </body>
</html>
```

Cada iframe:

- Tem seu próprio **DOM (Document Object Model) separado**
- Carrega seu próprio HTML, CSS e JavaScript
- Pode ser de um domínio diferente (cross-origin)
- Opera em um contexto de navegação isolado

### Por que Você Não Pode Interagir Diretamente

Este código **não funcionará** como você espera:

```python
# Isso NÃO encontrará elementos dentro do iframe
button = await tab.find(id='button-inside-iframe')
```

**Por quê?** Porque `tab.find()` pesquisa no **DOM da página principal**. O iframe tem um **DOM completamente separado** que não é acessível a partir do pai.

Pense desta forma:

```
DOM da Página Principal         DOM do IFrame (Separado!)
├── <html>                    ├── <html>
│   ├── <body>                │   ├── <body>
│   │   ├── <div>             │   │   ├── <div>
│   │   └── <iframe>          │   │   └── <button id="inside">
│   │       (mundo separado)  │   └── </body>
│   └── </body>               └── </html>
└── </html>
```

!!! info "Contextos de Navegação Isolados"
    IFrames criam o que é chamado de **contexto de navegação isolado**. Esse isolamento é um recurso de segurança que impede que iframes maliciosos acessem ou manipulem o conteúdo da página pai.

### Como o Pydoll Resolve Isso

Nos bastidores, o Pydoll usa o Chrome DevTools Protocol (CDP) para:

1.  **Identificar o alvo (target) do iframe**: Cada iframe obtém seu próprio ID de alvo CDP
2.  **Criar uma nova instância de Tab**: Esta Tab é escopada para o DOM do iframe
3.  **Fornecer acesso total**: Todos os métodos de Tab funcionam no DOM isolado do iframe

```python
# É isso que acontece internamente:
iframe_element = await tab.find(tag_name='iframe')  # Encontra a tag <iframe>
frame = await tab.get_frame(iframe_element)         # Obtém o alvo CDP para o iframe

# Agora 'frame' é uma Tab que opera no DOM do iframe
button = await frame.find(id='button-inside-iframe')  # Funciona!
```

### Análise Profunda Técnica: Alvos (Targets) CDP

Quando você chama `tab.get_frame()`, o Pydoll:

1.  **Extrai o atributo `src`** do elemento iframe
2.  **Consulta o CDP por todos os alvos** usando `Target.getTargets()`
3.  **Corresponde a URL do iframe** para encontrar seu ID de alvo correspondente
4.  **Cria uma instância de Tab** com esse ID de alvo

Cada alvo tem:

- **ID de Alvo Único**: Identifica o contexto de navegação
- **Conexão WebSocket Separada**: Para comunicação CDP isolada
- **Árvore de Documento Própria**: Independência completa do pai

```python
# Internamente em tab.py:
async def get_frame(self, frame: WebElement) -> Tab:
    # Obter a URL de origem do iframe
    frame_url = frame.get_attribute('src')
    
    # Encontrar o alvo que corresponde a esta URL
    targets = await self._browser.get_targets()
    iframe_target = next((t for t in targets if t['url'] == frame_url), None)
    
    # Criar uma Tab para o alvo deste iframe
    target_id = iframe_target['targetId']
    tab = Tab(self._browser, target_id=target_id, ...)
    
    return tab  # Agora você pode interagir com o iframe como uma Tab!
```

!!! warning "IFrame Deve Ter `src` Válido"
    O iframe deve ter um atributo `src` válido para o Pydoll localizar seu alvo CDP. IFrames usando `srcdoc` ou conteúdo injetado dinamicamente podem não funcionar com `get_frame()`.

## Comparação: Página Principal vs IFrame

| Aspecto | Página Principal | IFrame |
|---|---|---|
| **DOM** | Árvore de documento própria | Árvore de documento separada |
| **Alvo CDP** | Um ID de alvo | ID de alvo diferente |
| **Busca de Elemento** | `tab.find()` | `iframe.find()` |
| **Contexto JavaScript** | `window` da página principal | `window` do iframe |
| **Origem** | Origem da página | Pode ser cross-origin |
| **Armazenamento** | Compartilhado com a página | Pode ser isolado |

## Capturas de Tela em IFrames

!!! info "Limitações de Captura de Tela"
    `tab.take_screenshot()` só funciona em **alvos de nível superior**. Para capturas de tela de iframes, use `element.take_screenshot()` em elementos **dentro** do iframe.

```python
import asyncio
from pydoll.browser.chromium import Chrome

async def iframe_screenshot():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to('https://example.com/iframe-page')
        
        iframe_element = await tab.find(tag_name='iframe')
        frame = await tab.get_frame(iframe_element)
        
        # Isso não funcionará para iframes
        # await frame.take_screenshot('frame.png')
        
        # Em vez disso, capture um elemento dentro do iframe
        content = await frame.find(id='content')
        await content.take_screenshot('iframe-content.png')

asyncio.run(iframe_screenshot())
```

## Aprenda Mais

Para um entendimento mais profundo da mecânica de iframes e alvos CDP:

- **[Análise Profunda: Domínio da Aba](../../deep-dive/tab-domain.md#iframe-handling)**: Detalhes técnicos sobre a resolução de alvos de iframe
- **[Análise Profunda: Domínio do Navegador](../../deep-dive/browser-domain.md#target-management)**: Como o CDP gerencia múltiplos alvos
- **[Localização de Elementos](../element-finding.md#scoped-search)**: Entendendo o escopo do DOM na busca de elementos

IFrames podem parecer complexos, mas a API do Pydoll torna o trabalho com eles tão fácil quanto com elementos de página regulares. A chave é entender que cada iframe é sua própria Tab isolada, com um DOM e um alvo CDP separados.