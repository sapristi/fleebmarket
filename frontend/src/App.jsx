import React from "react";
import { useBottomScrollListener } from 'react-bottom-scroll-listener';
import './App.css';
import 'bulma/css/bulma.css'
/* import { Provider } from 'react-redux' */
import {  useSetRecoilState } from 'recoil';
import {
  SearchBox,  ResultsFetcher,  ItemsResultsFetcher } from './components/searchBox'
import {ResultsPanel} from './components/resultsPanel'
import { scrolledBottomTriggerState } from "atoms"
import {AdvertModal} from 'components/card'
import { BottomIndicator } from 'components/bottom_indicator'


export const App = () => {

    const triggerScrolled = useSetRecoilState(scrolledBottomTriggerState)

    useBottomScrollListener(() => { triggerScrolled(state => !state)}, {
        offset: 0,
        debounce: 200,
        triggerOnNoScroll: false
    })

    return (
          <div>
            <SearchBox search_type="advert"/>
            <React.Suspense fallback={<div>Loading...</div>}>
              <ResultsPanel/>
              <AdvertModal/>
              <ResultsFetcher/>
            </React.Suspense>
            <BottomIndicator search_type="advert"/>
          </div>
  );
}

export const ItemsApp = () => {

  const triggerScrolled = useSetRecoilState(scrolledBottomTriggerState)

  useBottomScrollListener(() => { triggerScrolled(state => !state)}, {
    offset: 0,
    debounce: 200,
    triggerOnNoScroll: false
  })

  return (
    <div>
      <SearchBox search_type="advert_item"/>
      <React.Suspense fallback={<div>Loading...</div>}>
        <ResultsPanel/>
        <AdvertModal/>
        <ItemsResultsFetcher/>
      </React.Suspense>
      <BottomIndicator search_type="advert_item"/>
    </div>
  );
}
