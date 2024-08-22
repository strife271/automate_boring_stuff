#! python3
# comic_auto_downloader.py - Downloads comics from multiple sites. Can be run by Windows Task Scheduler

# Instructions for project:
#
# Write a program that checks the websites of several web comics and automatically downloads the images
# if the comic was updated since the program’s last visit.
# Your operating system’s scheduler (Scheduled Tasks on Windows, launchd on macOS, and cron on Linux)
# can run your Python program once a day. The Python program itself can download the comic and then copy
# it to your desktop so that it is easy to find.
# This will free you from having to check the website yourself to see whether it has updated.

# Get a list of comic home page url. Check comic_image full path directory for the image file for each url,
# if the filename is not found download the image to the directory

# TODO Add more urls and create task in Task Scheduler
# Currently works correctly for 'https://xkcd.com'
# Unable to get other pages to work correctly

import requests
import os
import bs4
from pathlib import Path


def download_comics(comic_info: dict, comic_path: Path):
    for url, my_selector in comic_info.items():

        # Download the page.
        print('Downloading page %s...' % url)
        res = requests.get(url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        # Find the URL of the comic image.
        comicElem = soup.select(my_selector) # Different for each web page some do
        if comicElem == []:
            print('Could not find comic image.')
        else:

            comicUrl = 'https:' + comicElem[0].get('src')

            # Check to see if file is in directory
            image_path = os.path.join(comic_path, os.path.basename(comicUrl))
            if not os.path.exists(image_path):

                # Download the image.
                print('Downloading image %s...' % (comicUrl))
                res = requests.get(comicUrl)
                res.raise_for_status()

                # Save the image to .comic_path.
                imageFile = open(image_path, 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
            else:
                print(f'No new image for {url} found.')


if __name__ == "__main__":

    # store comics in correct directory
    save_directory = Path(r"C:\Users\mount\PycharmProjects\automate_the_boring_stuff\chapter17_time\comic_images")
    os.makedirs(save_directory, exist_ok=True)

    # websites to check
    url_dict = {'https://xkcd.com': '#comic > img'}


    download_comics(url_dict, save_directory)
