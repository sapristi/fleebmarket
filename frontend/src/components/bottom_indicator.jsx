import React from "react";
import { useRecoilValue } from 'recoil';
import { resultsEndState } from 'atoms';
import { useSearchAppend } from 'hooks/search';

export const BottomIndicator = () => {
  const resultsEnd = useRecoilValue(resultsEndState);
  const searchAppend = useSearchAppend();

  const indicator =
        (resultsEnd)
        ? (<div className="notification is-primary is-light">No more results</div>)
        : (<button
             onClick={searchAppend}
             className="button is-primary is-light">Load more results</button>)
  ;
  return <div style={{display: "flex", justifyContent: "space-around"}}>{indicator}</div>
}
