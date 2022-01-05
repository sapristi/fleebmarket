import React from "react";
import {
  atom,
  selector,
  useRecoilState,
  useRecoilValue,
} from 'recoil';
import {
  ResultItemPreview, ResultItemModal, Mapping
} from 'components/resultItems';
import {SearchResultItem} from 'types';
import { asyncDebounce } from "utils";
import { searchInputState, searchResultsState, scrolledBottomTriggerState, uiPrefsState } from "atoms";
import { useSearchAppend, useSearchReplace } from 'hooks/search';
import { AdTypes } from 'common/defs';

const axios = require('axios').default;


const Regions = {
  "-": "",
  CA: "CA",
  EU: "EU",
  OTHER: "OTHER",
  US: "US"
}



export const ResultsFetcher = () => {
  const scrolledTrigger = useRecoilValue(scrolledBottomTriggerState);
  const searchAppend = useSearchAppend();
  const searchReplace = useSearchReplace();
  const searchInput = useRecoilValue(searchInputState);

  React.useEffect(() => {
    searchAppend();
  }, [scrolledTrigger]);

  React.useEffect( ()=> {
    searchReplace();
      }, [searchInput]);
  return null;
};

export const SearchBox = ({}) => {
  const [input, setInput] = useRecoilState(searchInputState);
  const [uiPrefs, setUIPrefs] = useRecoilState(uiPrefsState);
  const handleInputChange = (key) => (event) => {
    const value = event.target.value;
    setInput(prev => ({
      ...prev,
      [key]: value,
    }));
  };
  const handleShowImages = (event) => {
    if (event.type === "change") {
      setUIPrefs(prev => ({...prev, showImages: !prev.showImages}));
    }
  };

  return (
    <div style={{display: "flex", flexDirection: "row", alignItems: "end", flexWrap: "wrap"}}>
      <div style={{flexGrow: 2, marginRight: "0.5em"}}>
        <input className="input is-primary is-large"
               type="text"
               value={input.terms}
               onChange={handleInputChange("terms")}
               placeholder="search..."
        />
      </div>

      <div>
        <label className="label">Advert type</label>
        <div className="select">
          <select value={input.ad_type} onChange={handleInputChange("ad_type")}>
            {
              Object.entries(AdTypes).map(([key, {display}]) =>
                <option key={key} value={key}>{display}</option>)
            }
          </select>
        </div>
      </div>
      <div>
        <label className="label">Region</label>
        <div className="select">
          <select value={input.region} onChange={handleInputChange("region")}>
            {
              Object.entries(Regions).map(([key, value]) =>
                <option key={value} value={value}>{key}</option>)
            }
          </select>
        </div>
      </div>
    <div className="field">
      <input id="switchRoundedOutlinedDefault" type="checkbox" name="switchRoundedOutlinedDefault" className="switch is-rounded is-outlined is-rtl" checked={uiPrefs.showImages} onChange={handleShowImages}/>
      <label htmlFor="switchRoundedOutlinedDefault">Show preview</label>
    </div>
    </div>
  );
};

