import React from "react";
import { mdparser } from 'utils/reddit_parser'
import {
  atom,
  useRecoilState,
  useSetRecoilState
} from 'recoil';

import { ImageEmbed } from "../imgur_embed"
import {tagColors, TimestampSpan, AuthorTag, OPTag, LocationSpan, ItemTitle} from "./common"

import {selectedCardState} from "atoms"

const get_advert_terms = (ad_type, extra) => {
  if ((["Selling", "Sold", "Trading"])
    .includes(ad_type)) {
    return {
      main: [extra.offers, "Offers"],
      secondary: [extra.wants, "Wants"]
    }
  } else if ((["Buying", "Purchased"])
    .includes(ad_type)) {
    return {
      main: [extra.wants, "Wants"],
      secondary: [extra.offers, "Offers"]
    }
  } else {
    return { main: [extra.title_stripped], secondary: null }
  }
}


const PreviewItemTitle = ({ ad_type, author, reddit_id }) => {
  const ad_type_color = tagColors[ad_type];
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
        <OPTag reddit_id={reddit_id} className="tag"/>
      </div>
    </header>
  )
}


export const AdvertCard = (item) => {
  /**
     Card that displays one advert
   **/

  const setSelectedItem = useSetRecoilState(selectedCardState)

  const html = mdparser(item.full_text)

  console.log(item)
  const { reddit_id, created_utc, extra, ad_type, author } = item;
  const { main, secondary } = get_advert_terms(ad_type, extra);

  const handleClick = () => {
    setSelectedItem({ ...item, html, main, secondary })
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
