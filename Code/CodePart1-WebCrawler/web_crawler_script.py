import web_crawler

def initialize_crawler(article_list, directory_name, lan_char):
    seed_url_list = []

    for article in article_list:
        seed_url_list.append(f"https://{lan_char}.wikipedia.org/wiki/{article}")

    crawler = web_crawler.WebCrawler(seed_urls=seed_url_list,
                                     allowed_domains=[f"{lan_char}.wikipedia.org"],
                                     crawl_id=directory_name,
                                     max_pages=60,
                                     language=lan_char)
    crawler.crawl()
    print(f"Crawling completed. Data saved in {crawler.repository_path}/ and {crawler.report_file}")


def main():
    #Spanish Language List
    spanish_article_list = ["James_Whale",
                            "Hollywood",
                            "Nueva_York"]
    initialize_crawler(article_list=spanish_article_list, lan_char="es", directory_name="Spanish_Wikipedia_Test")
    #English Language List
    english_article_list = ["Main_Page",
                            "American_Revolutionary_War",
                            "Whitehead's_trogon"]
    initialize_crawler(article_list=english_article_list, lan_char="en", directory_name="English_Wikipedia_Test")

    #German Language List
    german_article_list = ["Paris",
                           "Industrialisierung",
                           "E-Sport"]
    initialize_crawler(article_list=german_article_list, lan_char="de", directory_name="German_Wikipedia_Test")

if __name__ == "__main__":
    main()


