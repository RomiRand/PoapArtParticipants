# PoapArtParticipants
A tool to identify all drawing participants of a custom area on app.poap.art

__________
Sometimes people want to find out who helped drawing their images (for example to reward them with a poap).
This (very small and very simple) tool allows you to do this with pixel-level accuracy. 

You need python3 and some common libraries.

# How to use
1. Clone the repo
2. Run: `python3 getParticipants.py <your canvas id>` \
   You can find the canvas id by navigating to the canvas on poap.art and looking at the url bar.
3. Select pixels by holding `s` while moving your mouse (I know that feels weird, dumb reasons, I'm sorry).
   Selected Pixels will turn red as an indicator.
4. Once you're happy, hit `p` to gather the addresses. This might take a while,
   you can follow progress on console.
5. Press `q` to quit.


## Known issues
- It's slow, expect to wait a little for large images
- Only works for app.poap.art (not sandbox)