# Albert Plugins
This is a collection of plugins I made for Albert launcher. For now they don't
do much other than offering suggestions and opening them on the browser when
selected, but I plan on adding more functionalities, as well as more plugins.


## Requirements
The YouTube plugin requires [chromix-too](https://github.com/smblott-github/chromix-too).
That is used for replacing any existing YouTube tab with the one you create.
Chromix requires the installation of an extension, running a server, and using a
client to send the commands. For the server I created a systemd script to run it
automatically whenever I start my pc. The script looks like this.

```
[Unit]
Description=Chromix too

[Service]
User=zxcv
ExecStart=/bin/chromix-too-server

[Install]
WantedBy=multi-user.target
```

BeautifulSoup4 is also required for the YouTube plugin, and it's used to parse the
response page to get the links and titles of videos. You can install it using:

```bash
pip install beautifulsoup4
```

The `albert_trigger.sh` script requires xdotool, this script is used to open
albert with a certain query/trigger already in it.


## Descriptions
Here's a list of the plugins and a description of how they work.

**Google (gg)**
Get suggestions like the ones you get when searching on Google. When you select
an item the corresponding searchbar is opened in your default browser.

**YouTube (yt)**
Same as above but it's for YouTube. When you select an item a script is called
to prefix your query with an underscore. When searching with an underscore before
your query (eg: `yt \_panda dub`) you get a list of videos as results, and
selecting any one of them will replace any existing YouTube tab with that video
(it's definitely work in progress like the other plugins).

**Learn Anything (la)**
Get suggestions from [Learn Anything](https://learn-anything.xyz). For now you
only get the suggestions, but I plan on adding something similar to YouTube,
where you get a list of nodes/resources for each map when you select it.

**GitHub (gh)**
Search for a GitHub repo.

**Wordreference (enit)**
Get suggestions from Wordreference, I use it mostly when I'm not sure how to
spell a word, but if you select a word you can search for the translation. For
now it's only English to Italian or vice-versa, but I think it would be cool to
be able to set that in a config or just specify it on the query.


## Keybindings
You can find my keybindings on my [i3 config](https://github.com/nglgzz/dots/blob/laptop/config/i3/config)
but I'll go over the ones regarding Albert here. I remapped my spacebar to be
spacebar when pressed on its own, but Mod3 when pressed together with any other
key. This is accomplished by adding the following to `.xmodmaprc`:

```
keycode 65 = XF86Mail
keycode any = space
add mod3 = XF86Mail
```

You can use anything you want instead of `XF86Mail`, just check that it's a key
that you don't use. After that on your `.xinitrc` you should have two lines like
these:

```
xmodmap ~/.xmodmaprc
xcape -e "XF86Mail=space"
```

`xcape` is the program doing the magic I described before, and [here's](https://www.reddit.com/r/i3wm/comments/5zpz69/using_space_bar_as_mod_is_life_changing/)
a reddit post going more in detail on why you should use spacebar as a modifier.

The keybindings I have for these plugins are just calling `albert_trigger.sh` with
the trigger to use each plugin.

Here's the list of keybindings:

- **Space + b**: Toggle Albert
- **Space + g**: Google
- **Space + h**: GitHub
- **Space + y**: Youtube
- **Space + a**: Learn Anything
- **Space + e**: Wordreference
