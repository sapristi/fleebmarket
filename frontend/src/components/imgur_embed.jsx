import React from "react";
import { uiPrefsState } from "atoms";
import { useRecoilValue } from "recoil";

const get_timestamp_links = (links) =>
      links.filter(
        ({title}) => (
          title &&
          title.toLowerCase().includes("timestamp")
        )

      );

const get_imgur_links = (links) => {
  const album_re = /imgur\.com\/(a|gallery)\/(?<id>[a-z0-9A-Z]+)/;
  const image_re = /imgur\.com\/(?<id>[a-z0-9A-Z]+)/;
  const reducer = (result, item) => {
    const album_match = item.href.match(album_re);
    if (album_match) {return [...result, {...item, imgur_id: "a/" + album_match[2]}];}
    const image_match = item.href.match(image_re)
    if (image_match) {return [...result, {...item, imgur_id: image_match[1]}];}
    else { return result; }
  };
  return links.reduce(reducer, []);
};


const get_preview_item = (links) => {
  const timestamp_links = get_timestamp_links(links)
  if (timestamp_links.length > 0) {
    const imgur_links = get_imgur_links(timestamp_links)
    if (imgur_links.length > 0) {return imgur_links[0]}
    console.log("Could not find imgur for timestamp", timestamp_links)
  }
  const imgur_links = get_imgur_links(links);
  if (imgur_links.length > 0) {return imgur_links[0]}
  return null
}


const ImgurEmbedInner = ({preview_item}) => {
  React.useEffect( () => {

    var newScriptTag = document.createElement('script');
    /* newScriptTag.id = globalImgurEmbedScriptTagId; */
    newScriptTag.src = "//s.imgur.com/min/embed.js";
    newScriptTag.type = "text/javascript";
    newScriptTag.async = true;

    document.querySelector('body').appendChild(newScriptTag);
  })
  return (
    <div style={{marginLeft: "-15px"}}>
      <blockquote className="imgur-embed-pub" lang="en" data-id={preview_item.imgur_id} data-context="false" ></blockquote>
    </div>
  )
}

export const ImageEmbed  = ({links}) => {
  const uiPrefs = useRecoilValue(uiPrefsState)
  if (! uiPrefs.showImages) {return null}

  if (! links) {return null}
  const preview_item = get_preview_item(links)
  if (! preview_item) {return null}

  console.log("Embeding", links)
  return <ImgurEmbedInner preview_item={preview_item}/>
}

