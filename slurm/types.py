import enum

from typing import Optional, Self

class Category(enum.StrEnum):
    """Question category enum."""

    LITERATURE = "Literature"
    HISTORY = "History"
    SCIENCE = "Science"
    FINE_ARTS = "Fine Arts"
    RELIGION = "Religion"
    MYTHOLOGY = "Mythology"
    PHILOSOPHY = "Philosophy"
    SOCIAL_SCIENCE = "Social Science"
    CURRENT_EVENTS = "Current Events"
    GEOGRAPHY = "Geography"
    OTHER_ACADEMIC = "Other Academic"
    TRASH = "Trash"


class Subcategory(enum.StrEnum):
    """Question subcategory enum."""

    LITERATURE = "Literature"  # regular cats also included because of database quirks
    HISTORY = "History"
    SCIENCE = "Science"
    FINE_ARTS = "Fine Arts"
    RELIGION = "Religion"
    MYTHOLOGY = "Mythology"
    PHILOSOPHY = "Philosophy"
    SOCIAL_SCIENCE = "Social Science"
    CURRENT_EVENTS = "Current Events"
    GEOGRAPHY = "Geography"
    OTHER_ACADEMIC = "Other Academic"
    TRASH = "Trash"

    AMERICAN_LITERATURE = "American Literature"
    BRITISH_LITERATURE = "British Literature"
    CLASSICAL_LITERATURE = "Classical Literature"
    EUROPEAN_LITERATURE = "European Literature"
    WORLD_LITERATURE = "World Literature"
    OTHER_LITERATURE = "Other Literature"

    AMERICAN_HISTORY = "American History"
    ANCIENT_HISTORY = "Ancient History"
    EUROPEAN_HISTORY = "European History"
    WORLD_HISTORY = "World History"
    OTHER_HISTORY = "Other History"

    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    PHYSICS = "Physics"
    MATH = "Math"
    OTHER_SCIENCE = "Other Science"

    VISUAL_FINE_ARTS = "Visual Fine Arts"
    AUDITORY_FINE_ARTS = "Auditory Fine Arts"
    OTHER_FINE_ARTS = "Other Fine Arts"

    
class Tossup:
    """Tossup class."""

    def __init__(
        self: Self,
        question: str,
        formatted_answer: Optional[str],
        answer: str,
        category: Category,
        subcategory: Subcategory,
    ):
        self.question: str = question
        self.formatted_answer: str = formatted_answer if formatted_answer else answer
        self.answer: str = answer
        self.category: Category = category
        self.subcategory: Subcategory = subcategory
    
    def __str__(self: Self) -> str:
        return self.question


class Language(enum.StrEnum):
    """ Language codes available for translation. """

    AFRIKAANS           = "af"
    ALBANIAN            = "sq"
    AMHARIC             = "am"
    ARABIC              = "ar"
    ARMENIAN            = "hy"
    ASSAMESE            = "as"
    AYMARA              = "ay"
    AZERBAIJANI         = "az"
    BAMBARA             = "bm"
    BASQUE              = "eu"
    BELARUSIAN          = "be"
    BENGALI             = "bn"
    BHOJPURI            = "bho"
    BOSNIAN             = "bs"
    BULGARIAN           = "bg"
    CATALAN             = "ca"
    CEBUANO             = "ceb"
    CHINESE_SIMPLIFIED  = "zh-CN"
    CHINESE_TRADITIONAL = "zh-TW"
    CORSICAN            = "co"
    CROATIAN            = "hr"
    CZECH               = "cs"
    DANISH              = "da"
    DHIVEHI             = "dv"
    DOGRI               = "doi"
    DUTCH               = "nl"
    ENGLISH             = "en"
    ESPERANTO           = "eo"
    ESTONIAN            = "et"
    EWE                 = "ee"
    FILIPINO            = "fil"
    FINNISH             = "fi"
    FRENCH              = "fr"
    FRISIAN             = "fy"
    GALICIAN            = "gl"
    GEORGIAN            = "ka"
    GERMAN              = "de"
    GREEK               = "el"
    GUARANI             = "gn"
    GUJARATI            = "gu"
    HAITIAN             = "ht"
    HAUSA               = "ha"
    HAWAIIAN            = "haw"
    HEBREW              = "he"
    HINDI               = "hi"
    HMONG               = "hmn"
    HUNGARIAN           = "hu"
    ICELANDIC           = "is"
    IGBO                = "ig"
    ILOCANO             = "ilo"
    INDONESIAN          = "id"
    IRISH               = "ga"
    ITALIAN             = "it"
    JAPANESE            = "ja"
    JAVANESE            = "jv"
    KANNADA             = "kn"
    KAZAKH              = "kk"
    KHMER               = "km"
    KINYARWANDA         = "rw"
    KONKANI             = "gom"
    KOREAN              = "ko"
    KRIO                = "kri"
    KURDISH             = "ku"
    KYRGYZ              = "ky"
    LAO                 = "lo"
    LATIN               = "la"
    LATVIAN             = "lv"
    LINGALA             = "ln"
    LITHUANIAN          = "lt"
    LUGANDA             = "lg"
    LUXEMBOURGISH       = "lb"
    MACEDONIAN          = "mk"
    MAITHILI            = "mai"
    MALAGASY            = "mg"
    MALAY               = "ms"
    MALAYALAM           = "ml"
    MALTESE             = "mt"
    MAORI               = "mi"
    MARATHI             = "mr"
    MEITEILON           = "mni-Mtei"
    MIZO                = "lus"
    MONGOLIAN           = "mn"
    MYANMAR             = "my"
    NEPALI              = "ne"
    NORWEGIAN           = "no"
    NYANJA              = "ny"
    ODIA                = "or"
    OROMO               = "om"
    PASHTO              = "ps"
    PERSIAN             = "fa"
    POLISH              = "pl"
    PORTUGUESE          = "pt"
    PUNJABI             = "pa"
    QUECHUA             = "qu"
    ROMANIAN            = "ro"
    RUSSIAN             = "ru"
    SAMOAN              = "sm"
    SANSKRIT            = "sa"
    SCOTS               = "gd"
    SEPEDI              = "nso"
    SERBIAN             = "sr"
    SESOTHO             = "st"
    SHONA               = "sn"
    SINDHI              = "sd"
    SINHALA             = "si"
    SLOVAK              = "sk"
    SLOVENIAN           = "sl"
    SOMALI              = "so"
    SPANISH             = "es"
    SUNDANESE           = "su"
    SWAHILI             = "sw"
    SWEDISH             = "sv"
    TAGALOG             = "tl"
    TAJIK               = "tg"
    TAMIL               = "ta"
    TATAR               = "tt"
    TELUGU              = "te"
    THAI                = "th"
    TIGRINYA            = "ti"
    TSONGA              = "ts"
    TURKISH             = "tr"
    TURKMEN             = "tk"
    TWI                 = "ak"
    UKRAINIAN           = "uk"
    URDU                = "ur"
    UYGHUR              = "ug"
    UZBEK               = "uz"
    VIETNAMESE          = "vi"
    WELSH               = "cy"
    XHOSA               = "xh"
    YIDDISH             = "yi"
    YORUBA              = "yo"
    ZULU                = "zu"