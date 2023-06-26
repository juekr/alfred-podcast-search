# Search podcasts from Alfred productivity tool

**alfred-podcast-search**:
Search PodcastIndex, Taddy &amp; more directly from your favorite productivity app Alfred!


## What this does

TBA

## Prerequisites 

[Alfred Powerpack](https://www.alfredapp.com/powerpack/) is needed, Python3 and `requests` should be installed on your system – if `pip3 install requests` does not throw an error, your setuop yould be fine.

## Step 1: clone this repository and setup prerequisites

```bash
git clone git@github.com:juekr/alfred-podcast-search.git
pip install requests
# cd alfred-podcast-search
# python3 -m venv .venv
# source .venv/bin/activate
# pip install -r requirements.txt
```

## Step 2: get API access

### PodcastIndex

Go click yourself a free account: <https://api.podcastindex.org/> – you'll get a password an `API key` and an `API secret` via mail (remember your password, it seems like there is no password-reset function). You can also use this link and login to submit new podcast feeds to PodcastIndex.

📄 Documentation: <https://podcastindex-org.github.io/docs-api/#overview--example-code>

## Step 3: API credentials and basic configuration

Create an account and get API credentials – you can copy the template from `example.env` to `.env`: 

```
PODCASTINDEX_API_KEY=
PODCASTINDEX_API_SECRET=
```

## Step 3: Import AlfredWorkflow

You can just add the packed workflow into Alfred, but I'm happy describe what it does once installed. If you want to install it manually, you can follow this description, but don't forget to click on the little folder icon on the lower left after creating a new Alfred workflow – and putting the `api.py` script in this folder.

Starting with a `Blank Workflow` (icon by <https://recraft.ai):>

![[zzz_Anhänge/Make Podcast-Index and Taddy search available from Alfred.png]]

My workflow uses Alfred's `Script filter` as input trigger. I specified the trigger word `podcast`, but you can easily change that. Everything that comes after the trigger word, will be combined into one query parameter and fed to the Python script from this repo.

![[zzz_Anhänge/Make Podcast-Index and Taddy search available from Alfred-3.png]]

Here in the lower left is a button that opens the folder in which your script lives. You should put the `api.py` and your `.env` file here. Should be somewhere below `Alfred.alfredpreferences/workflows/...`

In the `script` textarea, you put the following:

```bash
query=$1

python3 api.py "$query"
```

Also, please click on `Run Behaviour` and change the second setting in a way, so it does not query the API after every character you type. This might seem convenient, but some API might limit the number of calls you can make in a certain time.

![[zzz_Anhänge/Make Podcast-Index and Taddy search available from Alfred-4.png]]

Hit `Close`.

Next, we have to determine what should happen with the results that are returned via the Python script. You can also activate the debugger on the upper right (the little bug icon) – then you're able to see what happens when the script runs in the background.

## License

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a

[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: <http://creativecommons.org/licenses/by-nc-sa/4.0/>
[cc-by-nc-sa-image]: <https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png>
[cc-by-nc-sa-shield]: <https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg>