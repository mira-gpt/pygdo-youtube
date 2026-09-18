# pygdo-youtube

`pygdo-youtube` records YouTube links posted to PyGDO connectors, fetches their
public metadata, announces the title, and keeps a searchable, likeable video
catalogue. Repeated posts increase the persistent **Times added** counter.

## Install

Clone this repository into `gdo/youtube`, then install the module:

```sh
./gdo_adm.sh install youtube
```

The module needs no YouTube API key. It reads the public page metadata with a
short timeout and falls back to the canonical video link when metadata cannot
be fetched.

## Use

- Post a `youtube.com`, `youtu.be`, `shorts`, `live`, or `embed` video URL in a
  connected chat. New videos are stored and announced once.
- `$youtube [search]` or `$yt [search]` lists stored videos. Search covers
  title and description.
- `$youtube.up <id>` or `$ytup <id>` likes a video through PyGDO Votes.

Only public metadata is fetched. The resolver does not execute page scripts or
use account cookies.
