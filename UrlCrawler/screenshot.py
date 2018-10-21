import os
import asyncio
from pyppeteer import launch

async def screenshot(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.setViewport({ 'width': 1366, 'height': 768})

    name = url.split('://')[1].split('/')[0]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    screenshot_dir = base_dir + '/screenshots/'
    if not os.path.exists(screenshot_dir):
      os.makedirs(screenshot_dir)

    await page.screenshot({'path': '{0}/{1}.png'.format(screenshot_dir, name)})
    await browser.close()

# asyncio.get_event_loop().run_until_complete(screenshot('https://google.de'))