/* eslint-disable @typescript-eslint/no-unused-vars */
import React from "react";
import { DateTime } from "luxon";
import { useBottomScrollListener } from 'react-bottom-scroll-listener';
import './App.css';
import 'bulma/css/bulma.css'
/* import { Provider } from 'react-redux' */
import { RecoilRoot, useSetRecoilState } from 'recoil';
import {
  SearchBox,  ResultsFetcher } from './components/searchBox'
import {ResultsPanel} from './components/results_panel'
import { scrolledBottomTriggerState } from "atoms"
import {ResultItemModal} from 'components/resultItems'
import { BottomIndicator } from 'components/bottom_indicator'


function App() {

    const ref = React.useRef<HTMLDivElement | null>(null)
    const triggerScrolled = useSetRecoilState(scrolledBottomTriggerState)

    useBottomScrollListener(() => { triggerScrolled(state => !state)}, {
        offset: 0,
        debounce: 200,
        triggerOnNoScroll: false
    })

    return (
          <div>
            <SearchBox/>
            <React.Suspense fallback={<div>Loading...</div>}>
              <ResultsPanel/>
              <ResultItemModal/>
              <ResultsFetcher/>
            </React.Suspense>
            <BottomIndicator/>
          </div>
  );
}

export default App;
