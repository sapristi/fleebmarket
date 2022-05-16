import logging
import re
from datetime import datetime
from typing import Any, Optional

import mistune
from dateutil import tz
from praw.models import Submission as PrawSubmission
from pydantic import BaseModel
from search_app.models import RedditAdvert, RedditAdvertType

logger = logging.getLogger(__name__)
markdown_ast = mistune.create_markdown(renderer=mistune.AstRenderer())


class ParsedTitle(BaseModel):
    region: str
    country: str
    offers: str
    wants: str


def parse_mechmarket_title(title):
    try:
        m = re.match(r"\[(.*?)\].*?\[H\](.*?)\[W\](.*)", title)
        if m is None:
            raise Exception(f"Couldn't parse title {title}")
        country = m.group(1).strip()
        offers = m.group(2).strip()
        wants = m.group(3).strip()

        split_country = country.split("-")
        if len(split_country) == 2:
            region = split_country[0]
            country = split_country[1]
        else:
            region = "OTHER"
        return ParsedTitle(country=country, region=region, offers=offers, wants=wants)
    except Exception:
        return None


class ParsedTitleSimple(BaseModel):
    title_stripped: str


def parse_mechmarket_title_simple(title):
    m = re.match(r"\[(.*?)\](.*)", title)
    if m is None:
        return None
    return ParsedTitleSimple(title_stripped=m.group(2).strip())


class Link(BaseModel):
    href: str
    title: Optional[str]


def extract_md_ast(ast, links):
    node_text = ast.get("text", " ")
    # handle edge-case where children is a single string
    if "children" in ast:
        if isinstance(ast["children"], str):
            node_text += ast["children"]
        else:
            for node in ast["children"]:
                node_text += extract_md_ast(node, links)
    if ast["type"] == "link":
        links.append(Link(href=ast["link"], title=node_text.strip(" \n")))
    return node_text


url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"


def extract_links_from_text(text: str):
    matches = re.findall(url_regex, text)
    return [match[0] for match in matches]


class ParsedBody(BaseModel):
    text: str
    links: list[Link]


def parse_mechmarket_body(body):
    body_ast = markdown_ast(body)
    links = []
    text = extract_md_ast({"children": body_ast, "type": "root"}, links)
    text = text.replace("&#x200B", "").replace("\x00", "").strip(" \n")

    links_hrefs = [l.href for l in links]
    text_links_all = extract_links_from_text(text)
    text_links_extra = [link for link in text_links_all if link not in links_hrefs]
    links.extend([Link(href=l, title=None) for l in text_links_extra])

    return ParsedBody(text=text, links=links)


def parse_submission_extra(submission: PrawSubmission) -> Optional[dict[str, Any]]:
    if submission.link_flair_text in [
        RedditAdvertType.Selling,
        RedditAdvertType.Buying,
        RedditAdvertType.Sold,
        RedditAdvertType.Purchased,
        RedditAdvertType.Trading,
        RedditAdvertType.Traded,
    ]:
        parsed_title = parse_mechmarket_title(submission.title)
    else:
        parsed_title = parse_mechmarket_title_simple(submission.title)

    if parsed_title is None:
        return None
    parsed_body = parse_mechmarket_body(submission.selftext)

    return {**parsed_title.dict(), **parsed_body.dict()}


def parse_submission(submission: PrawSubmission) -> Optional[RedditAdvert]:
    if submission.author is None:
        return None

    if submission.link_flair_text is None:
        logger.info(
            "Submission without flair: [%s] %s", submission.id, submission.title
        )
        # TODO: check creation date. If too old, discard; else, keep as is
        return None

    if submission.selftext == "[removed]":
        logger.info("Submission was removed: [%s] %s", submission.id, submission.title)
        return None

    if not submission.link_flair_text in RedditAdvertType.to_parse():
        return None

    extra = parse_submission_extra(submission)
    if extra is None:
        logger.warning(
            "Cannot parse extra from submission: [%s] %s",
            submission.id,
            submission.title,
        )
        return None

    created_utc_dt = datetime.utcfromtimestamp(submission.created_utc).replace(
        tzinfo=tz.UTC
    )

    reddit_advert = RedditAdvert(
        reddit_id=submission.id,
        title=submission.title,
        ad_type=submission.link_flair_text,
        created_utc=created_utc_dt,
        author=submission.author.name,
        full_text=submission.selftext,
        extra=extra,
    )

    return reddit_advert
