### nugscraper

A tool to download files from nugs.net. Will only work with shows that you've purchased!

The nugs.net live music provider has a bulk download tool for Windows and OSX, but none for Linux. I got tired of having to click "download" a ton of times, or use a third-party add-on like DownThemAll, so I decided to write this tool to do it for me.  


### usage

Invoke the tool by calling `nugscraper` from the command line. You'll need to copy and paste the link from a "download all" window for usage in this tool.

```
Usage: nugscraper [OPTIONS]

Options:  
  -u, --url TEXT           URL of 'download all' window. Can be used multiple times to scrape more than one page.  [required]  
  -d, --dest-dir TEXT      Destination for downloaded files  [required]  
  -n, --num-procs INTEGER  Number of download processes [default: 3]  
  --help                   Show this message and exit.  
```
 
For now, nugscraper won't do the following:
 - rename files; the filename on nugs is what it will be downloaded as
 - split out files by date; you can download multiple albums from 