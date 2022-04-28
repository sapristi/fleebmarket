import React from "react";
import {
  useRecoilState,
  useRecoilValue,
} from 'recoil';
import { searchInputState,  scrolledBottomTriggerState, uiPrefsState } from "atoms";
import { useSearchAppend, useSearchReplace } from 'hooks/search';
import { useSearchItemAppend, useSearchItemReplace } from 'hooks/search_item';
import { AdTypes } from 'common/defs';



const Regions = {
  "-": "",
  CA: "CA",
  EU: "EU",
  OTHER: "OTHER",
  US: "US"
}
const SoldStatus = {
  Unsold: "false",
  Sold: "true",
  Any: "",
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



export const ItemsResultsFetcher = () => {
  const scrolledTrigger = useRecoilValue(scrolledBottomTriggerState);
  const searchItemAppend = useSearchItemAppend();
  const searchItemReplace = useSearchItemReplace();
  const searchInput = useRecoilValue(searchInputState);

  React.useEffect(() => {
    searchItemAppend();
  }, [scrolledTrigger]);

  React.useEffect( ()=> {
    searchItemReplace();
  }, [searchInput]);
  return null;
};

const AdTypeSelect = ({ad_type, handleInputChange}) => {
  return (
  <div>
    <label className="label">Advert type</label>
    <div className="select">
      <select value={ad_type} onChange={handleInputChange("ad_type")}>
        {
          Object.entries(AdTypes).map(([key, {display}]) =>
            <option key={key} value={key}>{display}</option>)
        }
      </select>
    </div>
  </div>
  )
}

const RegionSelect = ({region, handleInputChange}) => {
  return (
    <div>
      <label className="label">Region</label>
      <div className="select">
        <select value={region} onChange={handleInputChange("region")}>
          {
            Object.entries(Regions).map(([key, value]) =>
              <option key={value} value={value}>{key}</option>)
          }
        </select>
      </div>
    </div>
  )
}


const SoldStatusSelect = ({sold, handleInputChange}) => {
  return (
    <div>
      <label className="label">Sold</label>
      <div className="select">
        <select value={sold} onChange={handleInputChange("sold")}>
          {
            Object.entries(SoldStatus).map(([key, value]) =>
              <option key={value} value={value}>{key}</option>)
          }
        </select>
      </div>
    </div>
  )
}


const ShowPreviewToggle = () => {
  const [uiPrefs, setUIPrefs] = useRecoilState(uiPrefsState);
  const handleShowImages = (event) => {
    if (event.type === "change") {
      setUIPrefs(prev => ({...prev, showImages: !prev.showImages}));
    }
  };

  return (
    <div className="field">
      <input id="switchRoundedOutlinedDefault" type="checkbox" name="switchRoundedOutlinedDefault" className="switch is-rounded is-outlined is-rtl" checked={uiPrefs.showImages} onChange={handleShowImages}/>
      <label htmlFor="switchRoundedOutlinedDefault">Show preview</label>
    </div>
  )
}

export const SearchBox = ({search_type}) => {
  const [input, setInput] = useRecoilState(searchInputState);
  const [uiPrefs, setUIPrefs] = useRecoilState(uiPrefsState);
  const handleInputChange = (key) => (event) => {
    const value = event.target.value;
    setInput(prev => ({
      ...prev,
      [key]: value,
    }));
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
      {
        search_type === "advert" &&
          <AdTypeSelect ad_type={input.ad_type} handleInputChange={handleInputChange}/>
      }
      <RegionSelect region={input.region} handleInputChange={handleInputChange}/>
      {
      search_type === "advert_item" &&
          <SoldStatusSelect sold={input.sold}  handleInputChange={handleInputChange}/>
      }
      {
        search_type === "advert" &&
          <ShowPreviewToggle/>
      }
    </div>
  );
};

