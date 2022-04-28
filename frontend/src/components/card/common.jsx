
import { DateTime } from "luxon";
export const tagColors = {
  "Selling": "#5b92fa",
  "Buying": "#f5b400",
  "Trading": "#9f46f2",
  "Group Buy": "#669999",
  "Vendor": "#FF851B",
  "Service": "#FFC0CB",
  "Interest Check": "#ba6251",
  "Artisan": "#aca13f",
  "Bulk": "#CC6A15",
  "Sold": "#dc4437",
  "Purchased": "#dc4437"
}

export const TimestampSpan = ({ created_utc }) => {
  const createdDate = DateTime.fromISO(created_utc);
  return <time key="time" className="card-footer-item" dateTime={createdDate.toISO()}>{createdDate.toLocaleString(DateTime.DATETIME_FULL)}</time>;
}

export const AuthorTag = ({ author, classExtra }) => {
  classExtra = classExtra || "";
  const className = `tag ${classExtra}`;
  return (
    <span className={className}><a href={`https://reddit.com/u/${author}`}>by /u/{author}</a></span>
  )
}
export const OPTag = ({ reddit_id, className }) => {
  return (
    <span className={className}><a href={`https://reddit.com/${reddit_id}`}>See on /r/mechmarket</a></span>
  )
}
export const LocationSpan = ({ extra }) => {
  if (!extra.country) { return null; }
  return (
    <span key="location" className="card-footer-item">
      {extra.region}-{extra.country}
    </span>
  )
}

export const ItemTitle = ({ ad_type, author, reddit_id }) => {
  return (
    <div style={{
      flexGrow: 2, marginRight: "10px", alignItems: "center",
      display: "flex", flexDirection: "column"
    }}>
      <span className="modal-card-title">{ad_type}</span>
      <div style={{display: "flex", flexDirection: 'row', justifyContent: "space-between", width: "100%"}}>
        <AuthorTag author={author} classExtra="is-medium" />
        <OPTag reddit_id={reddit_id} className="tag is-medium"/>
      </div>
    </div>
  )
}

