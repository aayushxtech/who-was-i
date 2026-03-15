import random

adjectives = list(
    set(
        [
            "brave",
            "calm",
            "delightful",
            "eager",
            "faithful",
            "gentle",
            "happy",
            "jolly",
            "kind",
            "lively",
            "nice",
            "obedient",
            "proud",
            "silly",
            "thankful",
            "victorious",
            "witty",
            "zealous",
            "bold",
            "cheerful",
            "daring",
            "elegant",
            "fierce",
            "friendly",
            "glad",
            "graceful",
            "honest",
            "humble",
            "joyful",
            "keen",
            "lucky",
            "merry",
            "noble",
            "optimistic",
            "patient",
            "playful",
            "polite",
            "quick",
            "quirky",
            "radiant",
            "reliable",
            "smart",
            "spirited",
            "steady",
            "thoughtful",
            "upbeat",
            "valiant",
            "warm",
            "wise",
            "zesty",
        ]
    )
)

animals = list(
    set(
        [
            "ant",
            "bear",
            "cat",
            "dog",
            "elephant",
            "fox",
            "giraffe",
            "hippo",
            "iguana",
            "jaguar",
            "kangaroo",
            "lion",
            "monkey",
            "newt",
            "owl",
            "panda",
            "quokka",
            "rabbit",
            "snake",
            "turtle",
            "urchin",
            "vulture",
            "wolf",
            "xenops",
            "yak",
            "zebra",
        ]
    )
)


def generate_display_name() -> str:
    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    number = random.randint(0, 99)
    if random.random() < 0.5:
        return f"{adjective.capitalize()}{animal.capitalize()}{number:02d}"
    else:
        return f"{animal.capitalize()}{adjective.capitalize()}"
