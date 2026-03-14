import random
import string
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Tuple
from datetime import datetime, timezone
import uuid

from app.models.room import Room
from app.core.security import hash_password, verify_password

prefix = ["room", "chat"]

words = list(
    set(
        [
            "avengers",
            "lakers",
            "nebula",
            "lantern",
            "cactus",
            "meteor",
            "sapphire",
            "voyager",
            "falcon",
            "ember",
            "glacier",
            "horizon",
            "pioneer",
            "quantum",
            "raven",
            "shadow",
            "tempest",
            "orbit",
            "zenith",
            "matrix",
            "cosmos",
            "harbor",
            "pixel",
            "rocket",
            "atlas",
            "breeze",
            "comet",
            "delta",
            "echo",
            "forest",
            "galaxy",
            "halo",
            "island",
            "jungle",
            "keystone",
            "legend",
            "mirage",
            "nova",
            "oasis",
            "phoenix",
            "quartz",
            "radar",
            "solstice",
            "titan",
            "utopia",
            "vector",
            "whisper",
            "xenon",
            "yonder",
            "zephyr",
            "asteroid",
            "blizzard",
            "cascade",
            "dynamo",
            "element",
            "fusion",
            "gravity",
            "harvest",
            "ignite",
            "journey",
            "kingdom",
            "labyrinth",
            "momentum",
            "nebulae",
            "odyssey",
            "paradox",
            "quest",
            "resonance",
            "spectrum",
            "trajectory",
            "uplink",
            "velocity",
            "wildfire",
            "xplorer",
            "yearling",
            "zodiac",
            "anchor",
            "beacon",
            "citadel",
            "drifter",
            "enigma",
            "frontier",
            "guardian",
            "haven",
            "insight",
            "junction",
            "kinetic",
            "lighthouse",
            "monolith",
            "network",
            "outpost",
            "protocol",
            "radiant",
            "sentinel",
            "terminal",
            "unison",
            "vortex",
            "adventure",
            "bliss",
            "dawn",
            "eclipse",
            "fable",
            "galore",
            "infinity",
            "kaleidoscope",
            "legendary",
            "miracle",
            "nirvana",
            "paradise",
            "quasar",
            "reverie",
            "serenity",
            "tranquility",
            "voyage",
            "wonder",
            "zen",
            "zeal",
            "aurora",
            "crystal",
            "dream",
            "flame",
            "glow",
            "harmony",
            "illusion",
            "jewel",
            "lore",
            "mystic",
            "prism",
            "radiance",
            "sanctuary",
            "twilight",
            "universe",
        ]
    )
)

characters = string.ascii_uppercase

# Room Joining Logic:

# Generate candidate room code


def _generate_room_code() -> str:
    return (
        random.choice(prefix)
        + "-"
        + random.choice(words)
        + "-"
        + "".join(random.choices(characters, k=4))
    )


# Ensure room code uniqueness
def generate_room_code(db: Session) -> str:
    while True:
        candidate = _generate_room_code()

        result = db.execute(select(Room).where(Room.room_code == candidate))

        existing_room = result.scalar_one_or_none()

        if not existing_room:
            return candidate


# Create room
def create_room(db: Session, password: str) -> Tuple[str, str]:
    """
    Create a new room and return (room_code, room_id)
    """

    room_code = generate_room_code(db)
    password_hash = hash_password(password)

    room = Room(
        id=uuid.uuid4(),
        room_code=room_code,
        password_hash=password_hash,
        created_at=datetime.now(timezone.utc),
        last_activity_at=datetime.now(timezone.utc),
        is_active=True,
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    return room.room_code, str(room.id)


# Joining Logic:


# Get room by code
def get_room_by_code(db: Session, room_code: str) -> Room | None:
    result = db.execute(select(Room).where(Room.room_code == room_code))

    return result.scalar_one_or_none()


# Validate room join


class RoomJoinError(Exception):
    """Base exception for room join validation errors."""


class RoomNotFoundError(RoomJoinError):
    pass


class RoomInactiveError(RoomJoinError):
    pass


class InvalidRoomPasswordError(RoomJoinError):
    pass


def validate_room_join(db: Session, room_code: str, password: str) -> Room:
    room = get_room_by_code(db, room_code)

    if not room:
        raise RoomNotFoundError("Room not found")

    if not room.is_active:
        raise RoomInactiveError("Room is not active")

    if not verify_password(password, room.password_hash):
        raise InvalidRoomPasswordError("Invalid password")

    return room


# Update room activity


def update_room_activity(db: Session, room: Room):
    room.last_activity_at = datetime.now(timezone.utc)

    db.add(room)
    db.commit()
