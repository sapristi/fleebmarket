export type SearchResultLink = {
    href: string;
    title: string;
}

type SearchResultExtra = {
    offers: string;
    wants: string;
    country: string;
    region: string;
    links: SearchResultLink[];
    title_stripped: string;
}



export type SearchResultItem = {
    reddit_id: string;
    ad_type: string;
    author: string;
    created_utc: string;
    extra: SearchResultExtra;
    full_text: string;
}
