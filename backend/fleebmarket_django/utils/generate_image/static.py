texts = [
    "Hey there, I'm the clicky one !",
    "Please touch me so softly.",
    "To click or not to click, that is the question.",
    "Wow, so many switches ! Very touchy, much smoothness",
    "It's raining keycaps !",
    "The keycaps profile you need right now ! ",
    "The pushback force is strong in this one.",
    "Amazing colors, great feeling, durable as rock.",
    "Lubed by hand for extra smoothness",
    "Split and tenting, that's my way to be",
    "Useless but essential, allow yourself to be tempted by my handcrafter overpriced artisan !",
    "It feels like typing on a cloud of boobs",
    "After this, you'll never touch a rubber dome again",
    "These new switches will make you type twice as fast",
    "So low profile, you won't even notice it"
]

template = """
<style>
 body {{background-color: {background_color};}}
 .front {{
     margin: 0;
     position: absolute;
     top: 50%;
     left: 50%;
     -ms-transform: translate(-50%, -50%);
     transform: translate(-50%, -50%);
     width: 80%;
     color: {text_color}
 }}
 span {{
     font-size: 3rem;
     font-family: Cantarell;
     font-weight: bolder;
 }}
</style>
<div class="back">
  <div class="front">
  <span>
     {text}
  </span>
  </div>
</div>
"""

palettes = [
    ('222831', '393e46', '00adb5', 'eeeeee'),
    ('f9ed69', 'f08a5d', 'b83b5e', '6a2c70'),
    ('f38181', 'fce38a', 'eaffd0', '95e1d3'),
    ('08d9d6', '252a34', 'ff2e63', 'eaeaea'),
    ('e3fdfd', 'cbf1f5', 'a6e3e9', '71c9ce'),
    ('364f6b', '3fc1c9', 'f5f5f5', 'fc5185'),
    ('a8d8ea', 'aa96da', 'fcbad3', 'ffffd2'),
    ('ffc7c7', 'ffe2e2', 'f6f6f6', '8785a2'),
    ('f9f7f7', 'dbe2ef', '3f72af', '112d4e'),
    ('e4f9f5', '30e3ca', '11999e', '40514e'),
    ('ffb6b9', 'fae3d9', 'bbded6', '61c0bf'),
    ('2b2e4a', 'e84545', '903749', '53354a'),
    ('defcf9', 'cadefc', 'c3bef0', 'cca8e9'),
    ('00b8a9', 'f8f3d4', 'f6416c', 'ffde7d'),
    ('f67280', 'c06c84', '6c5b7b', '355c7d'),
    ('e23e57', '88304e', '522546', '311d3f'),
    ('48466d', '3d84a8', '46cdcf', 'abedd8'),
    ('ffcfdf', 'fefdca', 'e0f9b5', 'a5dee5'),
    ('a8e6cf', 'dcedc1', 'ffd3b6', 'ffaaa5'),
    ('212121', '323232', '0d7377', '14ffec'),
    ('bad7df', 'ffe2e2', 'f6f6f6', '99ddcc'),
    ('ffc8c8', 'ff9999', '444f5a', '3e4149'),
    ('2d4059', 'ea5455', 'f07b3f', 'ffd460'),
    ('3ec1d3', 'f6f7d7', 'ff9a00', 'ff165d'),
    ('6fe7dd', '3490de', '6639a6', '521262'),
    ('a1eafb', 'fdfdfd', 'ffcef3', 'cabbe9'),
    ('8ef6e4', '9896f1', 'd59bf6', 'edb1f1'),
    ('f0f5f9', 'c9d6df', '52616b', '1e2022'),
    ('303841', '00adb5', 'eeeeee', 'ff5722'),
    ('f7fbfc', 'd6e6f2', 'b9d7ea', '769fcd'),
    ('1b262c', '0f4c75', '3282b8', 'bbe1fa'),
    ('d4a5a5', 'ffecda', 'f9ffea', 'a6d0e4'),
    ('07689f', 'a2d5f2', 'fafafa', 'ff7e67'),
    ('dcedc2', 'ffd3b5', 'ffaaa6', 'ff8c94'),
    ('f85f73', 'fbe8d3', '928a97', '283c63'),
    ('a8e6cf', 'fdffab', 'ffd3b6', 'ffaaa5'),
    ('384259', 'f73859', '7ac7c4', 'c4edde'),
    ('1fab89', '62d2a2', '9df3c4', 'd7fbe8'),
    ('f5eee6', 'f3d7ca', 'e6a4b4', 'c86b85'),
    ('00e0ff', '74f9ff', 'a6fff2', 'e8ffe8')
]
