# Albert Plugins
This is a collection of plugins I made for Albert launcher.

![img](https://thumbs.gfycat.com/BlondLinedGnatcatcher-max-14mb.gif)


## Requirements
`lxml` is required for the Google plugin. It is used for parsing the results
pages. It can be installed by running:

```bash
pip install lxml
```

The `albert_trigger.sh` script requires xdotool, this script is used to open
albert with a certain query/trigger already in it.


## Descriptions
Here's a list of the plugins and a description of how they work.

**Google (gg)**
Get suggestions like the ones you get when searching on Google. When you select
an item the corresponding results page is opened in your default browser. If you
append `_` to your query you'll get the results directly on albert
(eg: `gg unixporn reddit_`), and selecting any of the results will open it with
your default browser.

**YouTube (yt)**
Same as above but it's for YouTube. When searching with an underscore after
your query (eg: `yt panda dub_`) you get a list of videos as results, and
selecting any one of them will open that video with your default browser.

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
