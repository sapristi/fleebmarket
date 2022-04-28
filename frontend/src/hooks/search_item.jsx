import {
  useSetRecoilState,
  useRecoilState,
  useRecoilValue,
} from 'recoil';
import { fl_host, cookies } from 'common/defs';
import { searchInputState, searchResultsState, resultsEndState } from "atoms";
import { asyncDebounce } from "utils";

const axios = require('axios').default;



const doSearchItemBase = async (input, offset) => {
  const headers = {};
  if (cookies.csrftoken) {headers["X-CSRFToken"] = cookies.csrftoken;}
  const response = await axios.get(fl_host + '/api/search_item/',  {params:{
    terms: input.terms,
    region: input.region,
    sold: input.sold,
    limit: 9,
    offset: offset,
  }},{
    headers: headers,
  });
  return response.data;
};


const doSearchItem = asyncDebounce(doSearchItemBase, 100);

export const useSearchItemAppend = () => {
  const searchInput = useRecoilValue(searchInputState);
  const [searchResults, setSearchResults] = useRecoilState(searchResultsState);
  const setResultsEnd = useSetRecoilState(resultsEndState);

  console.log("Search Item hook")
  const resFun= () => doSearchItem(searchInput, searchResults.length)
        .then(
          res => {
            setResultsEnd(res.length===0);
            setSearchResults(prev => {
              /* Handles double requests;
                there should be a better way
              */
              const prev_keys = prev.map(p => p.id);
              const filtered_res = res.filter(r => (! prev_keys.includes(r.id)));
              return [...prev, ...filtered_res];
            });
          }
        );
  return resFun;
};


export const useSearchItemReplace = () => {
  const searchInput = useRecoilValue(searchInputState);
  const setSearchResults = useSetRecoilState(searchResultsState);
  const setResultsEnd = useSetRecoilState(resultsEndState);

  const resFun = () => doSearchItem(searchInput, 0).then(res => {
    setResultsEnd(res.length===0);
    setSearchResults(res);
  });
  return resFun;
};
