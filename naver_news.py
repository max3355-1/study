from playwright.sync_api import Playwright, sync_playwright
import csv

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.naver.com')
    page.type('#query', '삼쩜삼')
    page.click('#search_btn')
    page.wait_for_selector('body')
    page.click('.lnb_menu > ul > li.menu > a:has-text(\"뉴스\")')
    page.wait_for_selector('body')

    news_articles = []
    for i in range(2):
        page.wait_for_selector('body')
        news = page.query_selector('.group_news')
        news_links = news.query_selector_all('.list_news> li > div > div > a')
        for link in news_links[:20]:
            title = link.text_content()
            url = link.get_attribute('href')
            news_articles.append({'title': title, 'url': url})
            if len(news_articles) >= 20:
                break
        try:
            page.click(f'.sc_page_inner > a:nth-child({i + 2})')
        except:
            break

    browser.close()

with open('naver_news.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for article in news_articles:
        writer.writerow(article)
