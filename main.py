"""A single sentence about the best meal ever eaten.

The brief asks for one sentence, at most two hundred characters, on the
best meal the writer ever had. Twelve sentences were drafted by hand,
each one graded out of ten on three axes -- how vivid the scene feels,
how intimate the memory is, and how long the line stays with the reader
after it ends. The program ranks them by total marks, breaks ties in
favour of the shorter line, and writes the winner to /output/entry.txt.

The winning line went through a genuine second pass. Its first version
closed by explaining what freshness meant, which told the reader what to
think instead of letting the bite do the work. The rewrite leads with the
bite itself, puts juice on the chin, and closes on a chase that is still
going on years later, so the ending is a habit rather than a lesson.
"""

from pathlib import Path

OUT = Path("/output/entry.txt")
LIMIT = 200
STOPS = ".!?"


DRAFTS = [
    {
        "line": "My grandmother's kitchen smelled of garlic and woodsmoke the night she set down a bowl of hand-pulled noodles, and I ate until the broth was gone and the room went quiet.",
        "vivid": 9, "intimate": 9, "echo": 8,
        "note": "Garlic, smoke, an emptied bowl: a full scene, though the quiet room at the end is a little staged.",
    },
    {
        "line": "At a plastic table in Taipei at 2am, I ate beef noodle soup so hot it fogged my glasses, and the vendor laughed when I asked for a second bowl.",
        "vivid": 9, "intimate": 9, "echo": 9,
        "note": "Two in the morning, fogged glasses, a laughing vendor: place, heat and a human beat in one breath.",
    },
    {
        "line": "The best meal I ever had was a paper plate of fried fish my father cooked on a beach fire, salt on my lips, sand between my toes, the sun going down behind us.",
        "vivid": 8, "intimate": 8, "echo": 8,
        "note": "Salt, sand and a beach fire are vivid, but the paper plate and the sunset lean on familiar pictures.",
    },
    {
        "line": "In a tiny Lisbon tasca, the waiter brought grilled sardines still hissing from the charcoal, and I squeezed lemon over them with hands that smelled of the sea all evening.",
        "vivid": 9, "intimate": 8, "echo": 8,
        "note": "Sardines hissing off charcoal is a strong image; the voice reads more like a travel note than a memory.",
    },
    {
        "line": "My mother made congee with century egg and shredded chicken the morning I came home sick from school, and I still measure every comfort against that first warm spoonful.",
        "vivid": 9, "intimate": 9, "echo": 9,
        "note": "A sick day, a named dish, a first warm spoonful: deeply personal, and the ending turns comfort into a yardstick.",
    },
    {
        "line": "On a train through the mountains, a stranger shared her lunchbox of cold rice balls wrapped in seaweed, and I have never tasted anything so generous.",
        "vivid": 7, "intimate": 9, "echo": 9,
        "note": "Generous and true, but the meal itself is thin on senses; the generosity carries more weight than the food.",
    },
    {
        "line": "The oyster I ate raw at a stall in Guangzhou, briny and cold, with a drop of lemon and a dash of chili, made the whole noisy market fall silent for one second.",
        "vivid": 9, "intimate": 7, "echo": 8,
        "note": "Brine, lemon, chilli, a noisy market: vivid throughout, though a market falling silent overreaches.",
    },
    {
        "line": "At my sister's wedding, between the speeches, I stole a plate of roast duck in the kitchen, skin crackling, juice running down my chin, and hid laughing behind the door.",
        "vivid": 9, "intimate": 9, "echo": 8,
        "note": "Stolen duck, crackling skin, hiding and laughing: funny and personal, but the joke crowds the meal a little.",
    },
    {
        "line": "A bowl of ramen in a six-seat Tokyo shop, steam on my face, the egg yolk breaking gold into the broth, taught me that six square metres can hold the whole world.",
        "vivid": 8, "intimate": 7, "echo": 7,
        "note": "Steam and a gold yolk are concrete, yet the closing line about six square metres sounds ready-made.",
    },
    {
        "line": "The best meal I ever had was not in a restaurant but on my grandmother's porch, corn on the cob dripping butter, her laugh mixing with the cicadas at dusk.",
        "vivid": 8, "intimate": 8, "echo": 8,
        "note": "Butter, cicadas, a grandmother laughing: warm, though the not-a-restaurant framing is a familiar move.",
    },
    {
        "line": "I bit into a tomato still warm from my grandfather's garden, salt on my fingers and juice running down my chin, barefoot in the dirt, and I have chased that taste in every tomato since.",
        "vivid": 9, "intimate": 9, "echo": 10,
        "note": "WINNER. One tomato, still warm, salt, juice, bare feet: the smallest meal made the most specific, and the ending turns a single bite into a lifelong standard.",
    },
    {
        "line": "After eighteen hours without food on a delayed flight, a flight attendant slipped me a still-warm bread roll, and I have never been so grateful for anything in my life.",
        "vivid": 6, "intimate": 9, "echo": 9,
        "note": "The gratitude is real, but a bread roll is too thin a meal to carry the title of best ever.",
    },
]  # twelve drafts, one winner


def total_marks(draft):
    return draft["vivid"] + draft["intimate"] + draft["echo"]


def within_brief(line):
    stripped = line.strip()
    if not stripped:
        return False
    if len(stripped) > LIMIT:
        return False
    if sum(stripped.count(mark) for mark in STOPS) != 1:
        return False
    return stripped[-1] in STOPS


def choose(drafts):
    for draft in drafts:
        if not within_brief(draft["line"]):
            raise ValueError("draft outside the brief: " + draft["line"][:40])
    ranked = sorted(drafts, key=lambda d: (-total_marks(d), len(d["line"])))
    return ranked[0]["line"]


def emit():
    picked = choose(DRAFTS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(picked, encoding="utf-8")
    back = OUT.read_text(encoding="utf-8")
    if back != picked:
        raise SystemExit("what landed on disk is not the chosen line")
    if not within_brief(back):
        raise SystemExit("what landed on disk fails the brief")
    print(picked)


if __name__.endswith("__main__"):
    emit()
