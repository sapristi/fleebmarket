import React from "react";
import { mdparser } from 'utils/reddit_parser'
import {
  atom,
  useRecoilState,
  useSetRecoilState
} from 'recoil';

import {tagColors, TimestampSpan, AuthorTag, OPTag, LocationSpan} from "./common"


export const AdvertItemCard = (item) => {
  /**
     Card that displays one advert
   **/

  const { id, reddit_id, price, sold, ad_type, created_utc, author, extra } = item;

  return (
    <div className="card"
         style={{width: "420px", margin: "10px",
                 display: "flex", flexDirection: "column"}}
    >
      <header className="card-header">
        <p className="card-header-title">
          { sold ? "sold": "unsold"}
        </p>
        <div className="card-header-icon">
          <span className="icon">
            <i className="fas fa-angle-down"></i>
          </span>
        </div>
      </header>
      <div className="card-content" style={{flexGrow: 1}}>

        <div dangerouslySetInnerHTML={{__html: item.full_text}} className="content" />
      </div>
      <div className="card-footer">

        <LocationSpan extra={extra} />
        <TimestampSpan created_utc={created_utc} />
      </div>
      <div className="card-footer">
        <span className="card-footer-item">{item.price}$</span>
        <OPTag reddit_id={reddit_id} className="card-footer-item"/>
      </div>

    </div>
  )
}
