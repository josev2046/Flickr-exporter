# Flickr exporter

A quick Python hack designed to archive a complete Flickr photostream at maximum quality while preserving all associated metadata.

## Overview
This script automates the retrieval of original files and data from the Flickr API. It is designed to ensure that every image is paired with a comprehensive JSON sidecar file containing community interactions and technical metadata.

## Features
* **Original Resolution**: Specifically targets the `url_o` source to ensure no compression is applied to the download.
* **Metadata Archival**: Generates a `.json` sidecar for every file containing:
    * **Core Data**: Titles, descriptions, and tags.
    * **Timestamps**: Date taken, date posted, and last update times.
    * **Social Data**: A full list of user comments including author names.
    * **Geographic Data**: Latitude and longitude coordinates where available.
* **Resume Capability**: Scans local storage before initiating downloads to prevent redundant data transfer.
* **Paginated Logic**: Automatically iterates through the entire collection in 500-photo increments.

## Prerequisites
* **Python 3.11+**
* **Flickr API Key and Secret**: Required for OAuth authentication.
* **Flickr Pro (Optional)**: Recommended for accessing original resolution files via the API.

## Execution
1. Open the script and enter your credentials into the `API_KEY` and `API_SECRET` variables.
2. Run the script via the terminal:
   `python3 download_flickr.py`
3. Follow the OAuth prompt to authorise the application in your browser.

## Data organisation
The script organises the backup into a flat directory structure:
* `downloads/`
    * `PHOTO_ID.jpg` (The original image file)
    * `PHOTO_ID.json` (The metadata sidecar)

## Logic flow
<img width="819" height="961" alt="image" src="https://github.com/user-attachments/assets/f04557bd-378e-467e-bbb9-5a33ff762062" />

The script verifies the OAuth token upon initiation. Once validated, it identifies the unique NSID and begins a loop through the `flickr.photos.search` endpoint. For every photo object returned, it cross-references the local directory to skip files already present.

## Disclaimer
This tool is intended for personal archival use. Users should ensure compliance with Flickr's API Terms of Service regarding rate limits and data usage.

