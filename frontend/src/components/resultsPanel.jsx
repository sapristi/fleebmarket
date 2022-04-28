import React from "react";
import {
  useRecoilValue,
} from 'recoil';
import {
  AdvertCard, AdvertItemCard
} from 'components/card';
import {  searchResultsState, } from "atoms";

const Card = (item) => {
  switch(item.type) {
  case "advert":
    return <AdvertCard {...item}/>
    break
  case "advert_item":
    return <AdvertItemCard {...item}/>
    break
  }
}

export const ResultsPanel = () => {
  const searchResults = useRecoilValue(searchResultsState);
  return (
    <div
      style={{display: "flex", flexWrap: "wrap"}}
    >
      {
        searchResults.map(
          res => <Card {...res} key={res.id}/>
        )
      }
    </div>
  );
};
