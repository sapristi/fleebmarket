# How fleebmarket came to be

I bought some keyboard parts, and realized that's not really what I wanted. So I looked online for a way to sell them, only to find the dready state of second-hand keyboard market!
(I must say I did'nt look really deep, but lists of adverts of any kind and from anywhere just felt very unefficient to me).

I could not let that last any longer, so I took my little fingers and started typing...

I chose the all so well established Django framework, because of all the facilities it provided, which allowed me to quickly iterate until a first prototype was ready. As for the name, fleebmarket came to my mind, which is kind of a play on words between « flea-market » and « keeb ».

----

I initialy tried to model all the different pieces that are used to build a keyboard, so as to provide a full-fledged form for advert creation. The goal was to provide fine grained search of particular parts.

But there were several difficulties to that:

 - Custom mechanical keyboards, are, well, *custom*. Every part can be swapped, modified, exist in various flavours and versions, not to mention personal mods. This make creating a generic database quite a huge challenge.
 - `/r/mechmarket` centralises most of the adverts, and it would have been extremely difficult to divert users into using fleebmarket.
 - I realized I didn't really wanted to provide a platform to manage transactions, since, well, transactions do not always end up as you expect them to be, which means manual work of conflict solving and moderation would have been needed at some point.

I am thus focusing for now on providing tools that do not involve supervising transactions.

