runSelenium:
    docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome

runScraper:
    docker build . -t scraper --rm
    docker run -d -v scraperVol:/app/data --rm --name scraper scraper