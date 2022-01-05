import React from "react";
import {mdparser, get_timestamp_image} from 'utils/reddit_parser'
import {SearchResultItem} from 'types';
import { DateTime } from "luxon";
import {
  atom,
  selector,
  useRecoilState,
  useRecoilValue,
  useSetRecoilState
} from 'recoil';
import { ImageEmbed } from "./imgur_embed"


type ResultItemFullProps = SearchResultItem & {
  html: string,
  main: string[],
  secondary: string[] | null,
}

type ItemModalProps = {
  data: ResultItemFullProps | null;
}

const selectedCardState = atom<null|ResultItemFullProps>({
  key: "selectedCard",
  default: null
})


export type Mapping = {
  [key: string]: string;
}

const tagColors : Mapping = {
  "Selling": "#5b92fa",
  "Buying": "#f5b400",
  "Trading": "#9f46f2",
  "Group Buy": "#669999",
  "Vendor": "#FF851B",
  "Service": "#FFC0CB",
  "Interest Check": "#ba6251",
  "Artisan": "#aca13f",
  "Bulk": "#CC6A15",
  "Sold": "#dc4437",
  "Purchased": "#dc4437"
}

const AuthorTag = ({author, classExtra}: any) => {
  classExtra = classExtra || "";
  const className = `tag ${classExtra}`;
  return (
    <span className={className}><a href={`https://reddit.com/u/${author}`}>by /u/{author}</a></span>
  )
}
const OPTag = ({reddit_id, classExtra}: any) => {
  classExtra = classExtra || "";
  const className = `tag ${classExtra}`;
  return (
    <span className={className}><a href={`https://reddit.com/${reddit_id}`}>See on /r/mechmarket</a></span>
  )
}
const LocationSpan = ({extra}: any) => {
  if (!extra.country) {return null;}
  return (
    <span key="location" className="card-footer-item">
      {extra.region}-{extra.country}
    </span>
  )
}

const TimestampSpan = ({created_utc}: any) => {
  const createdDate = DateTime.fromISO(created_utc);
  return <time key="time" className="card-footer-item" dateTime={createdDate.toISO()}>{createdDate.toLocaleString(DateTime.DATETIME_FULL)}</time>
}

const get_advert_terms = (ad_type: string, extra: any) => {
  if ((["Selling", "Sold", "Trading"]).includes(ad_type)) {
    return {
      main: [extra.offers, "Offers"],
      secondary: [extra.wants, "Wants"]
    }
  } else if ((["Buying", "Purchased"]).includes(ad_type)) {
    return {
      main: [extra.wants, "Wants"],
      secondary: [extra.offers, "Offers"]
    }
  } else {
    return {main: [extra.title_stripped], secondary: null}
  }
}


const ItemTitle= ({ad_type, author, reddit_id}: any) => {
  return (
    <div style={{
      flexGrow: 2, marginRight: "10px", alignItems: "center",
      display: "flex", flexDirection: "column"
    }}>
      <span className="modal-card-title">{ad_type}</span>
      <div style={{display: "flex", flexDirection: 'row', justifyContent: "space-between", width: "100%"}}>
        <AuthorTag author={author} classExtra="is-medium" />
        <OPTag reddit_id={reddit_id} classExtra="is-medium"/>
      </div>
    </div>
  )
}


export const ResultItemModal = () => {

  const [selectedCard, setSelectedCard] = useRecoilState(selectedCardState);
  /* const [isOpen, setOpen] = React.useState(false); */
  /* const [data, setData] = React.useState<null|ResultItemFullProps>(null); */
  const close = () => setSelectedCard(null);
  const handleKeyPress = (keyEvent: any) => {
    if (keyEvent.key == "Escape") {close()}
  }
  React.useEffect(() => {
    document.addEventListener("keydown", handleKeyPress, false);

    return () => {
      document.removeEventListener("keydown", handleKeyPress, false);
    };
  }, []);

  if (selectedCard === null) {return <></>}

  const {
    reddit_id, created_utc, extra, html, ad_type,
    main, secondary, author,
  } = selectedCard;


  const ad_type_color : string = tagColors[ad_type];
  return (
    <div className="modal is-active" onKeyPress={handleKeyPress}>
      <div className="modal-background" onClick={close} onKeyPress={handleKeyPress}></div>
      <div className="modal-card wide" onKeyPress={handleKeyPress}>
        <header className="modal-card-head"
                style={{backgroundColor: ad_type_color}}
        >
          <ItemTitle ad_type={ad_type} author={author} reddit_id={reddit_id} />
          <button className="delete" aria-label="close" onClick={close}></button>
        </header>
        <section className="modal-card-body">
          <div style={{
            display: "flex", flexDirection: 'row', justifyContent: "space-around",
            width: "100%", marginBottom: "10px", flexWrap: "wrap"
          }}>
            <div>
              {(main.length > 1) && main[1]+":"}
              <p className="title is-5">{main[0]}</p>
            </div>
            {
              secondary &&
              <div><span>{secondary[1]}:</span> <p className="title is-6">{secondary[0]}</p></div>
            }
          </div>
          <hr/>
          <div dangerouslySetInnerHTML={{__html: html}} className="content" />
        </section>
        <footer className="modal-card-foot">
          <LocationSpan extra={extra} />
          <TimestampSpan created_utc={created_utc} />
        </footer>
      </div>
    </div>
  )
}


const PreviewItemTitle= ({ad_type, author, reddit_id}: any) => {
  const ad_type_color : string = tagColors[ad_type];
  return (
    <header className="card-header"
            style={{
              backgroundColor: ad_type_color,
              display: "flex", flexDirection: "column",
              alignItems: "center", padding: "5px"
            }}
    >
      <span style={{fontWeight: 600}}>{ad_type}</span>
      <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", width: "100%"}}>
        <AuthorTag author={author}/>
        <OPTag reddit_id={reddit_id}/>
      </div>
    </header>
  )
}

interface ILink {
  href: string;
  title: string | null;
}


export const ResultItemPreview = (item : SearchResultItem) => {

  const setSelectedItem = useSetRecoilState(selectedCardState)

  const html = mdparser(item.full_text)

  const {reddit_id, created_utc, extra, ad_type, author} = item;
  const {main, secondary} = get_advert_terms(ad_type, extra);

  const handleClick = () => {
    setSelectedItem({...item, html, main, secondary})
  }


  return (
    <div className="card"
         style={{width: "420px", margin: "10px",
                 display: "flex", flexDirection: "column"}}
    >
      <PreviewItemTitle ad_type={ad_type} author={author} reddit_id={reddit_id} />
      <div className="card-content" style={{flexGrow: 1}} onClick={handleClick}>
        {(main.length > 1) && main[1]+":"}
        <p className="title is-5">{main[0]}</p>
        {
          secondary &&
          <><span>{secondary[1]}:</span> <p className="title is-6">{secondary[0]}</p></>
        }
        <ImageEmbed links={item.extra.links} />
        
      </div>
      <div className="card-footer">
        <LocationSpan extra={extra} />
        <TimestampSpan created_utc={created_utc} />
      </div>
    </div>
  )
}
