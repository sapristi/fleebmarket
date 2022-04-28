import { marked } from 'marked';

export const mdparser = (text): string => {
  let html = marked(text, []);

  html = html.replace(/<table>/g, '<table class="table is-striped is-hoverable">')
  html = html.replace(/<a/g, '<a target="blank"')
  return html;
}

export const get_timestamp_image = (links) => {
    for (var link of links) {
        // console.log(link)
        if (link.title.toLowerCase().includes('time')) {
            /* console.log("timestamp", link.href) */
            return link
        }
    }

}
