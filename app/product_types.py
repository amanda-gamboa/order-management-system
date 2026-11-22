from enum import StrEnum


class ProductType(StrEnum):
    """
    Defines the supported categories of digital products.

    Each member represents a general product category with
    a canonical string value used for API validation and
    database storage.
    """

    # Sound effects, voice recordings, and other non-musical audio.
    AUDIO = "audio"

    # Audiobooks and narrated books.
    AUDIOBOOK = "audiobook"

    # Structured educational content delivered online.
    COURSE = "course"

    # Digital documents, guides, and downloadable publications.
    DOCUMENT = "document"

    # Electronic books and written publications.
    EBOOK = "ebook"

    # Digital images, including photographs, illustrations, and AI-generated images.
    IMAGE = "image"

    # Access to exclusive digital content, perks, or online communities.
    MEMBERSHIP = "membership"

    # Applications designed for mobile devices.
    MOBILE_APP = "mobile_app"

    # Music tracks, albums, and other musical compositions.
    MUSIC = "music"

    # Extensions that add functionality to existing software.
    PLUGIN = "plugin"

    # Desktop applications, utilities, and general computer programs.
    SOFTWARE = "software"

    # Ongoing digital services provided via recurring billing.
    SUBSCRIPTION_SERVICE = "subscription_service"

    # Reusable templates for tools such as Notion, Excel, or presentations.
    TEMPLATE = "template"

    # Digital three-dimensional models and assets.
    THREE_D_MODEL = "3d_model"

    # Video content, including clips, films, animations, and recordings.
    VIDEO = "video"

    # Video games for computers, consoles, and mobile devices.
    VIDEO_GAME = "video_game"

    # Applications accessed through a web browser.
    WEB_APP = "web_app"
