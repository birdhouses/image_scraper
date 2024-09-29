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
