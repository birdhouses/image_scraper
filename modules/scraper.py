import re
import os
import pandas as pd
import scrapy
from multiprocessing import Process, Queue
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from concurrent.futures import ThreadPoolExecutor, as_completed

class BingImageSpider(scrapy.Spider):
    name = "bing_image_spider"

    def __init__(self, query, folder_name, *args, **kwargs):
        super(BingImageSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.folder_name = folder_name
        self.start_urls = [f"https://www.bing.com/images/search?q={query}"]

    def parse(self, response):
        # Extract image URLs using regex
        image_data = response.css('a.iusc::attr(m)').getall()
        image_urls = []
        for data_str in image_data:
            match = re.search(r'"murl":"(.*?)"', data_str)
            if match:
                image_url = match.group(1).replace('\\', '')
                image_urls.append(image_url)

        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)

        for idx, image_url in enumerate(image_urls):
            yield scrapy.Request(image_url, callback=self.save_image, meta={'idx': idx})

    def save_image(self, response):
        idx = response.meta['idx']
        image_data = response.body
        file_extension = response.url.split('.')[-1][:4]  # Limit to 4 chars to handle query strings
        filename = os.path.join(self.folder_name, f"{self.query}_{idx}.{file_extension}")
        with open(filename, 'wb') as f:
            f.write(image_data)

class ImageScraper:
    def process_single_image_search(self, topic, folder_name):
        """
        Process a single image search task.
        """
        try:
            self.scrape_images(topic, folder_name)
        except Exception as e:
            print(f"Error processing topic '{topic}': {e}")

    def scrape_images(self, query, folder_name):
        try:
            query = re.sub(r'[^a-zA-Z0-9 ]', '', query)

            # Use the modified process to handle reactor restart
            return self.run_spider(BingImageSpider, query=query, folder_name=folder_name)
        except Exception as e:
            print(f"Error scraping images for query '{query}': {e}")
            return "No images found"

    def run_spider(self, spider_class, *args, **kwargs):
        def spider_runner(queue):
            try:
                runner = CrawlerRunner()
                deferred = runner.crawl(spider_class, *args, **kwargs)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()
                queue.put(None)
            except Exception as e:
                queue.put(e)

        q = Queue()
        p = Process(target=spider_runner, args=(q,))
        p.start()
        result = q.get()
        p.join()

        if result is not None:
            raise result
        return {"status": "completed", "message": f"Scraping completed for query: {kwargs.get('query', '')}"}

    def process_image_search(self, csv_file_path='keywords.csv', workers=5, folder_name='downloaded_images'):
        try:
            if os.path.exists(csv_file_path):
                df = pd.read_csv(csv_file_path, on_bad_lines='skip')
            else:
                print(f"CSV file '{csv_file_path}' not found.")
                return {"status": "error", "message": f"CSV file '{csv_file_path}' not found."}

            # Invert the DataFrame (reverse the order of the rows)
            df = df.iloc[::-1].reset_index(drop=True)

            # Use ThreadPoolExecutor to process images in parallel
            with ThreadPoolExecutor(max_workers=workers) as executor:
                # Create a list of future tasks
                futures = [executor.submit(self.process_single_image_search, row['keyword'], folder_name) for _, row in df.iterrows()]

                # Process tasks as they complete
                for future in as_completed(futures):
                    try:
                        future.result(timeout=60)  # Adjust timeout as needed
                    except Exception as e:
                        print(f"Error processing task: {e}")
                        continue

            return {"status": "completed", "message": "Image search processed successfully"}
        except Exception as e:
            print(f"Error in process_image_search: {e}")
            return {"status": "error", "message": f"An error occurred while processing image search: {e}"}

if __name__ == '__main__':
    scraper = ImageScraper()
    result = scraper.process_image_search(csv_file_path='overwatch.csv', workers=5, folder_name='overwatch_images')
    print(result)
