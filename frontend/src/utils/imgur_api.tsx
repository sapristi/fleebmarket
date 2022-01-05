const axios = require('axios').default;

export const get_href_type = (href: string) => {
    const url = new URL(href)
    /* console.log(url) */
    if (url.host.includes("imgur")) {
        get_imgur_image(url)
    }
}

const get_imgur_image = (url: URL ) : string => {
    const path = url.pathname.split("/").filter(x => x)
    console.log(path)
    if (path.length === 1) {
        return url.href
    }
    if (path[0] === "a") {
        const album_id = path[1];
    }
    return url.href
}
