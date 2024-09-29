# Image Scraper Application

An image scraping application that downloads images from Bing based on keywords provided in a CSV file. The application leverages Scrapy and allows for concurrent downloading of images using multiprocessing and threading.
Scrape MILLIONS of images / day.

## Features

- **Keyword-Based Image Downloading**: Provide a list of keywords, and the application will download images related to those keywords.
- **Concurrent Processing**: Uses multiprocessing and threading to efficiently scrape images in parallel.
- **Customizable Output**: Specify the output folder where images will be saved.
- **Error Handling**: Robust error handling to ensure the application continues running even if some tasks fail.

## Requirements

- **Python 3.6+**
- **Scrapy**
- **Pandas**

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/image-scraper.git
   cd image-scraper
   ```

2. **Install Dependencies**

   Install the required Python packages:

   ```bash
   pip install scrapy pandas
   ```

   Ensure that you have `Scrapy`, `pandas`, and all their dependencies installed.

## Directory Structure

```
├── modules
│   └── scraper.py         # Contains the ImageScraper and BingImageSpider classes
├── app.py                 # Main script to run the image scraper
├── keywords.csv           # CSV file containing keywords (you need to create this)
├── downloaded_images      # Folder where images will be saved (created automatically)
```

## Usage

### 1. Prepare the CSV File

Create a CSV file named `keywords.csv` in the root directory. This file should contain a column named `keyword` with the list of keywords you want to search for.

**Example `keywords.csv`:**

```csv
keyword
Cat
Dog
Sunset
```

### 2. Configure `app.py`

In `app.py`, you can hardcode the CSV file path and the output folder name.

```python
# app.py

from modules.scraper import ImageScraper

if __name__ == '__main__':
    # Hardcode the CSV file path and output folder name here
    csv_file_path = 'keywords.csv'  # Replace with your CSV file path
    folder_name = 'downloaded_images'  # Replace with your desired output folder

    # Create an instance of the ImageScraper
    scraper = ImageScraper()

    # Call the process_image_search method with the hardcoded parameters
    result = scraper.process_image_search(csv_file_path=csv_file_path, workers=5, folder_name=folder_name)

    print(result)
```

Ensure that the `csv_file_path` points to your CSV file and `folder_name` is the directory where you want the images to be saved.

### 3. Run the Application

Execute the `app.py` script:

```bash
python app.py
```

The script will read the keywords from the CSV file and download images for each keyword into the specified folder.

### 4. Check the Output

After the script finishes running, you can find the downloaded images in the `downloaded_images` folder (or the folder name you specified).

## Advanced Usage

### Adjusting the Number of Workers

You can adjust the `workers` parameter in `app.py` to change the number of concurrent threads used for downloading images.

```python
result = scraper.process_image_search(csv_file_path=csv_file_path, workers=5, folder_name=folder_name)
```

Increasing the number of workers may speed up the downloading process but could also lead to being blocked by the target website if too many requests are made simultaneously.

### Changing the Search Engine

The application currently uses Bing for image searches. If you want to use a different search engine, you would need to modify the `BingImageSpider` class in `modules/scraper.py`.

## Dependencies

Ensure you have the following Python packages installed:

- **Scrapy**
- **Pandas**
- **Twisted** (installed automatically with Scrapy)
- **lxml** (used by Scrapy for parsing)

Install them using:

```bash
pip install scrapy pandas
```

## Legal and Ethical Considerations

- **Respect Website Policies**: Make sure you comply with Bing's terms of service and robots.txt policies when scraping images.
- **Copyright**: Be aware of copyright laws when downloading images. Use the images responsibly and ensure you have the rights or permissions to use them.
- **Usage of Images**: This application is intended for educational purposes. The developers are not responsible for any misuse of the downloaded images.

## Troubleshooting

- **CSV File Not Found**: If you receive an error stating that the CSV file is not found, ensure that the `csv_file_path` in `app.py` points to the correct file and that the file exists.
- **No Images Downloaded**: If no images are downloaded, check that your keywords are valid and that the search engine returns results for them.
- **Timeout Errors**: If you encounter timeout errors, you may increase the `timeout` value in `modules/scraper.py`:

  ```python
  future.result(timeout=60)  # Adjust timeout as needed
  ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Scrapy](https://scrapy.org/) - An open-source and collaborative framework for extracting the data you need from websites.
- [Pandas](https://pandas.pydata.org/) - An open-source data analysis and manipulation tool.
- [Bing](https://www.bing.com/) - For providing image search services.

---

**Note**: This application is intended for educational purposes. Please ensure you comply with all relevant laws and website terms of service when scraping data.