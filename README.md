# Scraping Project
This project was created for the University of Florida course, Advanced Web Apps. :cowboy_hat_face:
## What I wanted to get
I began working on this project with the idea that I would scrape disorganized data from the EPA's website. I went looking for anything I could find that would allow me to get data quickly instead of clicking on many, many links. The longest list of pages I found was on **Air Pollution**, violations under the *coal-fired power plant enforcement* section. ~~So I scraped it entirely and very easily.~~ The most critical information in the pages was the dollar amount in fines that these polluters had to pay to the government for their crimes. It would also be helpful to get more direct URLs to access documents linked on each page, such as the consent decree and formal complaints. Ultimately, my headings for the CSV file this data would print to became:
-The polluter's name
-The civil penalty paid by the polluter
-The consent decree, settling the legal dispute
-The formal complaint against the polluter by the U.S. government
-The page URL where the information was taken from
##How I did it
My code consists of three main functions:
1. To scrape the URLs and put them into a list
2. To scrape the information from each page
3. To run the above function for each page and print to a CSV file
###get_urls_from_single_page
This first function takes a base URL, where other URLs are listed. A for loop parses the page, finds the `a` tags in the `article` and appends each violation link to a list: `epa_url_list`. The list is returned and `get_urls_from_single_page` is called.
###scrape_violation
This is the meat of the project, and by far the most challenging to build. The name is scraped using a day 1 beautiful soup command: `soup.h1`. The PDF links were also grabbed very simply, using two for-loops for the consent decree and complaint. These for-loops look for the links using `'a', href=True` where the text contains the titles of these documents. But the real headache was the massive if-elif-else statement that looked for the civil penalties.
###write_csv
This last function is very simple. It writes the scraped information to a CSV, adds headings and closes the file. I added a sleep timer here, in case I ran into nay problems with a site not loading fast enough to be able to scrape it.
##Where I struggled
This HTML was a nightmare to work with. Because it seems this page was updated infrequently and only when the EPA had a big case to brag about, there were very little similarities in the pages' design. Finding the civil penalties was very difficult because of this. I intended to scrape the short paragraph that explained how much the polluter was fined and where that money went. In a perfect world, this text would be inside a `heading` tag. But the EPA's coders had many ways of storing this information:
-in an h2 or h3, with no id
-in a heading, but with id names such as `civil`, `penalty`, `penalties`, `civilpenalty` and even `mitigation`
-in a ul, with no other tags
-after a **strong** tag inside the same `p` tag
Because few of these text blocks were formatted in the same way, I had to find different ways to get what I was looking for. That culminated in a large if-elif-else block that looked for specific tags and text blocks that I identified with pages. Sometimes an `elif` worked for six pages, but sometimes it only worked for one. ***In conclusion, while this wasn't a very good build of a useful scraping tool, I learned more about to how scrape poorly formatted and difficult HTML than I would have while scraping most other sites.***
