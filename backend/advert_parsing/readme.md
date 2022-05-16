# Advert parsing

The goal here is to parse adverts: we want to extract
 1. the specific item to be sold
 2. its price
 3. whether it's already been sold


## Different problems

There are a few different cases to handle (although these cases likely overlap, so this could be refined):
- *case 0*: **the blob**
  All relevant text is in a single paragraph. Ok if there is a single price, otherwise will be difficult.
- *case 1*: **Paragraphs**
  Each item to be sold is in a dedicated paragraph.
- *case 2*: **Tables**
  The items to be sold are in a table.
  
The simplest case to handle is that of tables, because:
 - it's easy to spot
 - column are well separated, sometimes with headers
 
## Prepare parsing

The adverts are markdown (MD). In order to make them easier to work with, they are first transformed into a simple MD AST (see https://github.com/syntax-tree/mdast for example).

### Parse reddit markdown

Although it seems well specified, markdown is declined in many flavours, with (not fully specified) extensions being added (like tables). This means that not all md-parsing libraries will give the same results.
In the case of reddit markdown, I have mostly tried
 - mistune
   easy to extend in order to output custom ast; I started tweaking it to adapt to all reddit MD edgecases, but gave up on it.
 - misaka
   better support for reddit md tables (some cases are not handled by mistune). Needs a single tweak to be fully compatible with reddit MD.
   
The extracted AST contains:
- paragraphs
- separators
- lists
- tables
- text items, with optional strikethrough

Were ignored
- text style other than strikethrough

