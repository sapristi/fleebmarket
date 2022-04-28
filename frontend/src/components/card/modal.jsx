import React from "react";
import {
  atom,
  useRecoilState,
  useSetRecoilState
} from 'recoil';

import {selectedCardState} from "atoms"

import {tagColors, TimestampSpan, AuthorTag,  LocationSpan, ItemTitle} from "./common"

export const AdvertModal = () => {
  /**
     Modal that opens an advert full screen
   **/
  const [selectedCard, setSelectedCard] = useRecoilState(selectedCardState);
  /* const [isOpen, setOpen] = React.useState(false); */
  /* const [data, setData] = React.useState<null|ResultItemFullProps>(null); */
  const close = () => setSelectedCard(null);
  const handleKeyPress = (keyEvent) => {
    if (keyEvent.key === "Escape") { close() }
  }
  React.useEffect(() => {
    document.addEventListener("keydown", handleKeyPress, false);

    return () => {
      document.removeEventListener("keydown", handleKeyPress, false);
    };
  }, []);

  if (selectedCard === null) { return <></> }

  const {
    reddit_id,
    created_utc,
    extra,
    html,
    ad_type,
    main,
    secondary,
    author,
  } = selectedCard;

  const ad_type_color = tagColors[ad_type];
  return (
    <div className="modal is-active" onKeyPress={handleKeyPress}>
      <div className="modal-background" onClick={close} onKeyPress={handleKeyPress}></div>
      <div className="modal-card wide" onKeyPress={handleKeyPress}>
        <header className="modal-card-head"
                style={{backgroundColor: ad_type_color}}
        >
          <ItemTitle ad_type={ad_type} author={author} reddit_id={reddit_id} />
          <button className="delete" aria-label="close" onClick={close}></button>
        </header>
        <section className="modal-card-body">
          <div style={{
            display: "flex", flexDirection: 'row', justifyContent: "space-around",
            width: "100%", marginBottom: "10px", flexWrap: "wrap"
          }}>
            <div>
              {(main.length > 1) && main[1]+":"}
              <p className="title is-5">{main[0]}</p>
            </div>
            {
              secondary &&
              <div><span>{secondary[1]}:</span> <p className="title is-6">{secondary[0]}</p></div>
            }
          </div>
          <hr/>
          <div dangerouslySetInnerHTML={{__html: html}} className="content" />
        </section>
        <footer className="modal-card-foot">
          <LocationSpan extra={extra} />
          <TimestampSpan created_utc={created_utc} />
        </footer>
      </div>
    </div>
  )
}
