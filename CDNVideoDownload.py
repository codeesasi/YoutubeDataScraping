from playwright.sync_api import sync_playwright
import os,webbrowser

while True:
    VIDEO_PAGE_URL = input("Enter video page URL: ")
    DOWNLOAD_PATH = 'downloads'  # Folder where video will be saved

    # Make sure download folder exists
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    stream_urls = []
    brave_path = r'C:\Users\Sasi\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe'
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(
            headless=False,
            executable_path=brave_path,  # Launch Brave browser
            args=["--start-maximized"] )
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()

            def log_request(request):
                url = request.url
                if '.m3u8' in url or '.mp4' in url:
                    print("[Found Stream URL]:", url)
                    stream_urls.append(url)

            page.on("request", log_request)

            print("[*] Navigating to page...")
            page.goto(VIDEO_PAGE_URL)

            # Wait a bit more to ensure video loads
            page.wait_for_timeout(40000)

            # Wait for the element to be present
            page.wait_for_selector("xpath=/html/body/div[2]/div[2]/div[1]/h1")

            # Get text content
            text = page.locator("xpath=/html/body/div[2]/div[2]/div[1]/h1").inner_text()
            print(f"[*] Video name: {text}")

            # Filter for .mp4 direct video URL
            mp4_urls = [url for url in stream_urls if '.mp4' in url and 'cdn' in url]

            if mp4_urls:
                video_url = mp4_urls[0]  # Take first .mp4 URL
            
                webbrowser.open(video_url)

            browser.close()
        except Exception as e:
            print(f"Error: {e}")
