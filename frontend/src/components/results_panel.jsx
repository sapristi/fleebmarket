import React from "react";
import {
  atom,
  selector,
  useRecoilState,
  useRecoilValue,
} from 'recoil';
import {
  ResultItemPreview
} from 'components/resultItems';
import { searchInputState, searchResultsState, } from "atoms";


export const ResultsPanel = () => {
  const searchResults = useRecoilValue(searchResultsState);
  return (
    <div
      style={{display: "flex", flexWrap: "wrap"}}
    >
      {
        searchResults.map(
          res => <ResultItemPreview {...res} key={res.reddit_id}/>
        )
      }
    </div>
  );
};
