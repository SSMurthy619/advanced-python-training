# Import asyncio to manage the event loop and async tasks
import asyncio

# Import aiohttp to make asynchronous HTTP requests
import aiohttp


# Create a semaphore to limit concurrent requests
# This ensures only 5 requests run at the same time
sem = asyncio.Semaphore(5)


# Define an asynchronous function to fetch a single URL
async def fetch(session, url):
    # Acquire the semaphore before making a request
    async with sem:
        try:
            # Send a non-blocking HTTP GET request with a timeout
            async with session.get(url, timeout=10) as response:
                
                # Read the response body asynchronously as text
                html = await response.text()
                
                # Print useful information about the request
                print(f"URL: {url} | Status: {response.status} | Size: {len(html)} characters")
                
                # Return the fetched HTML (optional for further processing)
                return html

        # Catch any exception such as timeout or connection error
        except Exception as e:
            # Print the error without stopping the program
            print(f"URL: {url} | Error: {e}")
            
            # Return None when a failure occurs
            return None


# Define the main asynchronous entry point of the program
async def main():
    
    # Create a list of URLs to scrape (paginated pages)
    urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
        "https://quotes.toscrape.com/page/3/",
        "https://quotes.toscrape.com/page/4/",
        "https://quotes.toscrape.com/page/5/",
    ]

    # Create a single reusable HTTP client session
    async with aiohttp.ClientSession() as session:
        
        # Create a list of coroutine tasks for each URL
        tasks = [
            fetch(session, url) for url in urls
        ]

        # Run all fetch tasks concurrently and wait for completion
        await asyncio.gather(*tasks)


# Start the asyncio event loop and run the main function
# This is required to execute async code file from a script
asyncio.run(main())
