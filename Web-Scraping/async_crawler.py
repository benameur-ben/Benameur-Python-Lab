"""
Benameur Python Lab - Professional Series
Distributed Asynchronous Web Crawler
--------------------------------------
Author: Benameur Mohamed
Entity: Benameur Soft
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
import logging

# Configure Logging / إعداد سجل العمليات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BenameurCrawler:
    """
    A professional-grade asynchronous crawler capable of handling large-scale tasks.
    مستكشف ويب متطور يعمل بشكل غير متزامن للتعامل مع المهام واسعة النطاق.
    """
    
    def __init__(self, base_urls, concurrent_limit=5):
        self.base_urls = base_urls
        self.limit = concurrent_limit
        self.results = []
        self.semaphore = asyncio.Semaphore(concurrent_limit)

    async def fetch_page(self, session, url):
        """Fetches content from a URL with concurrency control / جلب المحتوى مع التحكم في التزامن"""
        async with self.semaphore:
            try:
                logger.info(f"🚀 Fetching: {url}")
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.text()
                        return await self.parse(url, content)
                    else:
                        logger.warning(f"⚠️ Failed {url} with status {response.status}")
            except Exception as e:
                logger.error(f"❌ Error at {url}: {str(e)}")
        return None

    async def parse(self, url, html):
        """Extracts metadata professionally / استخراج البيانات الوصفية بطريقة احترافية"""
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
        links = [a.get('href') for a in soup.find_all('a', href=True)][:5] # First 5 links
        data = {
            "url": url,
            "title": title.strip(),
            "links_count": len(links),
            "timestamp": time.time()
        }
        return data

    async def run(self):
        """Main execution flow / تدفق التنفيذ الرئيسي"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_page(session, url) for url in self.base_urls]
            self.results = await asyncio.gather(*tasks)
            logger.info(f"✅ Finished crawling {len(self.results)} targets.")
            return [r for r in self.results if r]

if __name__ == "__main__":
    # Example targets / أهداف تجريبية
    targets = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.python.org",
        "https://www.wikipedia.org"
    ]
    
    crawler = BenameurCrawler(targets)
    start_time = time.perf_counter()
    
    # Run the event loop / تشغيل حلقة الأحداث
    results = asyncio.run(crawler.run())
    
    end_time = time.perf_counter()
    print(f"\n--- Crawling Report (Benameur Soft) ---")
    for r in results:
        print(f"📍 {r['url']} | 🏷️ {r['title']}")
    print(f"\n⏱️ Total Time: {end_time - start_time:.2f} seconds")
