import React from "react";
import {
  useSetRecoilState,
  useRecoilState,
  useRecoilValue,
} from 'recoil';
import { AdTypes, fl_host, cookies } from 'common/defs';
import { searchInputState, searchResultsState, resultsEndState } from "atoms";
import { asyncDebounce } from "utils";

const axios = require('axios').default;


const doSearchBase = async (input, offset) => {
  const headers = {};
  if (cookies.csrftoken) {headers["X-CSRFToken"] = cookies.csrftoken;}
  const response = await axios.get(fl_host + '/api/search/',  {params:{
    terms: input.terms,
    limit: 9,
    offset: offset,
    type: AdTypes[input.ad_type]['payload'],
    region: input.region,
  }},{
    headers: headers,
  });
  return response.data;
};

const doSearch = asyncDebounce(doSearchBase, 100);

export const useSearchAppend = () => {
  const searchInput = useRecoilValue(searchInputState);
  const [searchResults, setSearchResults] = useRecoilState(searchResultsState);
  const setResultsEnd = useSetRecoilState(resultsEndState);

  const resFun= () => doSearch(searchInput, searchResults.length)
        .then(
          res => {
            setResultsEnd(res.length===0);
            setSearchResults(prev => {
              /* Handles double requests;
                there should be a better way
              */
              const prev_keys = prev.map(p => p.reddit_id);
              const filtered_res = res.filter(r => (! prev_keys.includes(r.reddit_id)));
              return [...prev, ...filtered_res];
            });
          }
        );
  return resFun;
};


export const useSearchReplace = () => {
  const searchInput = useRecoilValue(searchInputState);
  const setSearchResults = useSetRecoilState(searchResultsState);
  const setResultsEnd = useSetRecoilState(resultsEndState);

  const resFun = () => doSearch(searchInput, 0).then(res => {
    setResultsEnd(res.length===0);
    setSearchResults(res);
  });
  return resFun;
};
