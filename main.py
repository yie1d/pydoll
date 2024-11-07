import asyncio
import logging

from pydoll.browser.chrome import Chrome
from pydoll.browser.options import Options
from pydoll.constants import By
from pydoll.events.page import PageEvents


async def main():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--user-data-dir=/home/thalison/Documentos/beemon/pydoll/chrome_data')
    browser = Chrome(options=options)

    await browser.start()
    page = await browser.get_page()
    await page.go_to('https://tiktok.com')
    # verifica se logou

    if await page.wait_element(By.XPATH, '//span[text()="Carregar "]', timeout=10, raise_exc=False):
        print('Página logada')
        input()

    await page.go_to('https://www.tiktok.com/login/phone-or-email/email')
    input_email = await page.wait_element(By.CSS, 'input[name="username"]')
    await input_email.click()
    await input_email.send_keys('xeexieapmv@rambler.ru')
    input_password = await page.wait_element(By.CSS, 'input[placeholder="Senha"]')
    await input_password.click()
    await input_password.send_keys('!963o@!R')

    await asyncio.sleep(3)

    await (await page.wait_element(By.CSS, 'button[data-e2e="login-button"]')).click()


    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())
