## nugscraper

A tool to download files from nugs.net. Will only work with shows that you've purchased!

The nugs.net live music provider has a bulk download tool for Windows and OSX, but none for Linux. I got tired of having to click "download" a ton of times, or use a third-party add-on like DownThemAll, so I decided to write this tool to do it for me.  

### install

`nugscraper` isn't on PyPI yet. To install, clone the repository and use `pip`:

```bash
git clone https://github.com/tomplex/nugscraper.git
cd nugscraper
pip install .
```

### usage

Invoke the tool by calling `nugscraper` from the command line. You'll need to copy and paste the link from a "download all" window for usage in this tool.  

`nugscraper` requires your nugs.net username and password to log in and download your songs. Your username and password are not saved in any way. You can provide your credentials as environment variables, `NUGS_USERNAME` and `NUGS_PASSWORD`. If you do not set these variables, `nugscraper` will prompt for your username/password.


```
Usage: nugscraper [OPTIONS]

Options:  
  -u, --url TEXT           URL of 'download all' window. Can be used multiple times to scrape more than one page. [required]  
  -d, --dest-dir TEXT      Destination for downloaded files  [required]  
  -n, --num-procs INTEGER  Number of download processes [default: 3]  
  --help                   Show this message and exit.  
```
 
For now, nugscraper doesn't do the following:
 - rename files; the filename on nugs is what it will be downloaded as
 - split out files by date; you can download multiple albums from 