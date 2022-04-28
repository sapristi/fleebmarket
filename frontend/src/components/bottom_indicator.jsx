import React from "react";
import { useRecoilValue } from 'recoil';
import { resultsEndState } from 'atoms';
import { useSearchAppend } from 'hooks/search';
import { useSearchItemAppend } from 'hooks/search_item';


export const BottomIndicator = ({search_type}) => {
  const resultsEnd = useRecoilValue(resultsEndState);
  const searchAppend = useSearchAppend();
  const searchItemAppend = useSearchItemAppend();

  console.log("SEARCH TYPE", search_type)
  const search = (search_type == "advert") ? searchAppend : searchItemAppend

  const indicator =
        (resultsEnd)
        ? (<div className="notification is-primary is-light">No more results</div>)
        : (<button
             onClick={search}
             className="button is-primary is-light">Load more results</button>)
  ;
  return <div style={{display: "flex", justifyContent: "space-around"}}>{indicator}</div>
}
