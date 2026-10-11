#!/usr/bin/env python3
"""Builds astonify.com. Edit the text below, run `python3 build.py`, then push.

Rebuilt Oct 2026 from the last good copy of the old WordPress site (Internet Archive, Sept 2022),
updated to how the show is sold now: venues and private hosts hire it, in person (no more Zoom).
Rules for copy here: no em dashes, no prices, never describe how a routine works.
"""
import datetime
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PHONE = "703-404-8902"
PHONE_LINK = "tel:+17034048902"
EMAIL = "info@carnegiemagic.com"
SITE = "https://astonify.com/"
MAGO_FORM_ID = "e53a8875-e511-11ee-87d5-1a8035880eaa"  # same form as carnegiemagic.com/contact/

NAV = [("", "Home"), ("the-show/", "The Show"), ("christmas/", "Christmas"),
       ("about/", "About Carnegie"), ("book/", "Book the Show")]

SCHEMA = """<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {"@type": "WebSite", "@id": "https://astonify.com/#site", "url": "https://astonify.com/", "name": "The Astonify Show",
   "publisher": {"@id": "https://carnegiemagic.com/#dean"}},
  {"@type": "Person", "@id": "https://carnegiemagic.com/#dean", "name": "Dean Carnegie",
   "alternateName": "Carnegie, The Artist of Mystery", "jobTitle": "Illusionist and magic historian",
   "url": "https://carnegiemagic.com/", "image": "https://astonify.com/img/spirits-hero.jpg",
   "homeLocation": {"@type": "City", "name": "Nashville, Tennessee"},
   "sameAs": ["https://carnegiemagic.com/", "https://themagicdetective.com/", "https://magicdetectivepodcast.com/",
              "https://art.carnegiemagic.com/", "https://www.youtube.com/@ArtistofMystery"]},
  {"@type": "Service", "@id": "https://astonify.com/#show", "name": "The Astonify Show",
   "alternateName": "Astonify", "serviceType": "Victorian parlor magic show and theatrical seance",
   "description": "An immersive evening of Victorian parlor magic, thought reading and a theatrical seance, created and performed by Nashville illusionist Dean Carnegie for an intimate room of about fifty adults (ages 16 and up). Available all year for venues, museums, historic sites, clubs and private events.",
   "url": "https://astonify.com/", "image": "https://astonify.com/img/og.jpg",
   "provider": {"@id": "https://carnegiemagic.com/#dean"},
   "areaServed": [{"@type": "City", "name": "Nashville, Tennessee"}, {"@type": "State", "name": "Tennessee"}, {"@type": "Country", "name": "United States"}],
   "audience": {"@type": "PeopleAudience", "suggestedMinAge": 16},
   "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Astonify shows", "itemListElement": [
     {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "The Astonify Show", "url": "https://astonify.com/the-show/"}},
     {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Astonify: The Ghosts of Christmas Past", "url": "https://astonify.com/christmas/",
       "description": "A family friendly, Dickens inspired nineteenth century magic show for intimate December events."}}]},
   "review": [
     {"@type": "Review", "reviewBody": "Fun, Mystifying, Attention Grabbing! Our group thoroughly enjoyed seeing Dean Carnegie's Astonify Show.",
      "author": {"@type": "Person", "name": "Erin Clark", "jobTitle": "Executive Director, Fauquier History Museum at the Old Jail"}},
     {"@type": "Review", "reviewBody": "You gave a terrific performance, witty, colorful and fun as well as magical and confounding.",
      "author": {"@type": "Person", "name": "Dr. Donn B. Murphy", "jobTitle": "President, The National Theatre, Washington D.C."}}]}
 ]
}
</script>"""

# old WordPress addresses -> closest new page, so old links and Google listings still land somewhere useful
OLD_PAGES = {"home/": "", "synopsis/": "the-show/", "tour/": "the-show/", "bio/": "about/",
             "contact/": "book/", "holiday/": "christmas/", "privacy-policy/": "privacy/"}

REVIEWS = [
    ("Fun, Mystifying, Attention Grabbing!",
     "Our group thoroughly enjoyed seeing Dean Carnegie's Astonify Show, and could not stop talking about the various "
     "tricks he did. Dean was a pleasure to work with and easy to coordinate with. We look forward to seeing the show again!",
     "Erin Clark, Executive Director", "Fauquier History Museum at the Old Jail, Warrenton, Virginia"),
    ("Terrific Performance",
     "You gave a terrific performance, witty, colorful and fun as well as magical and confounding. How DID you do that?! "
     "In addition, you were not just easy to deal with offstage, but relaxed, genial and pleasant.",
     "Dr. Donn B. Murphy, President", "The National Theatre, Washington D.C."),
    ("So Different, So Fun",
     "The Astonify Show at The Secret Parlor Theatre was so different and yet it was so much fun! We had a great time "
     "and enjoyed the close-up show afterwards as well.",
     "Audience member", "The Secret Parlor Theatre, Chantilly, Virginia"),
    ("History and Magic in One",
     "I wasn't expecting a history lesson, but you hear so many true stories during the show that you come away "
     "smarter AND amazed!",
     "Audience member", "The Secret Parlor Theatre, Chantilly, Virginia"),
]

VIDEO_ID = "URUODQ2wFEM"  # The Astonify Show by Dean Carnegie (Dean chose this one, Oct 10 2026)

FAQ_SCHEMA = """<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "FAQPage",
 "mainEntity": [
  {
   "@type": "Question",
   "name": "What is The Astonify Show?",
   "acceptedAnswer": {
    "@type": "Answer",
    "text": "An immersive evening of Victorian parlor magic and thought reading, followed by a theatrical seance. It is created and performed by Dean Carnegie, a Nashville, Tennessee illusionist and magic historian, for an intimate room of about fifty guests."
   }
  },
  {
   "@type": "Question",
   "name": "Who is it for?",
   "acceptedAnswer": {
    "@type": "Answer",
    "text": "Adults. Astonify is designed for ages sixteen and up. In December there is a family friendly version, The Ghosts of Christmas Past."
   }
  },
  {
   "@type": "Question",
   "name": "Will I have to go on stage?",
   "acceptedAnswer": {
    "@type": "Answer",
    "text": "Only if you want to. Some mysteries involve the whole room at once, and others need a guest or two to step forward. Nobody is pushed into anything."
   }
  },
  {
   "@type": "Question",
   "name": "Is the seance real?",
   "acceptedAnswer": {
    "@type": "Answer",
    "text": "It is a theatrical seance, performed in the style of the nineteenth century parlor and presented as entertainment. It is slightly spooky, and it is part of the Astonify evening."
   }
  },
  {
   "@type": "Question",
   "name": "Is Astonify only in October?",
   "acceptedAnswer": {
    "@type": "Answer",
    "text": "No. The show is available all year, and different versions are offered through the year, including The Ghosts of Christmas Past in December."
   }
  },
  {
   "@type": "Question",
   "name": "Where is it performed?",
   "acceptedAnswer": {
    "@type": "Answer",
    "text": "Astonify is based in Nashville, Tennessee, and is available to travel. Venues, museums, historic sites, clubs and private hosts hire the show for an evening in their own room."
   }
  },
  {
   "@type": "Question",
   "name": "How do I book it?",
   "acceptedAnswer": {
    "@type": "Answer",
    "text": "Use the form on the Book the Show page, or call 703-404-8902. Tell us the date, the room and roughly how many guests."
   }
  }
 ]
}
</script>"""

SHOW_VIDEO_ID = "KJwryN8Tdjo"  # The Astonify Show Interview, on The Show page (Dean chose this one, Oct 10 2026)


def page(slug, title, description, body, extra_head="", body_end=""):
    root = "../" if slug else ""
    current = ' aria-current="page"'
    nav = "".join(
        f'<a href="{root}{s or "./"}"{current if s == slug else ""}>{label}</a>'
        for s, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{SITE}{slug}">
<link rel="icon" href="{root}img/icon.jpg">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="{SITE}img/og.jpg">
<meta property="og:url" content="{SITE}{slug}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
{extra_head}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="{root or './'}"><img src="{root}img/logo.png" alt="Astonify" width="180" height="55"></a>
    <nav aria-label="Main">{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <img src="{root}img/logo.png" alt="" width="200" height="61" class="foot-logo">
    <p class="foot-tag">Where Mysteries Abound</p>
    <p><a href="{PHONE_LINK}">{PHONE}</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p>The Astonify Show is produced by DAC Productions and Carnegie Magic, Nashville, Tennessee.<br>
    More about Dean Carnegie at <a href="https://carnegiemagic.com/">CarnegieMagic.com</a>.</p>
    <p class="small"><a href="{root}privacy/">Privacy</a> &middot; &copy; 2026 Carnegie Magic</p>
  </div>
</footer>
{body_end}
</body>
</html>
"""


def reviews_block():
    cards = "".join(f"""
    <figure class="review">
      <h3>{html.escape(h)}</h3>
      <blockquote>&ldquo;{html.escape(q)}&rdquo;</blockquote>
      <figcaption><strong>{html.escape(who)}</strong><br>{html.escape(where)}</figcaption>
    </figure>""" for h, q, who, where in REVIEWS)
    return f'<section class="band"><div class="wrap"><h2 class="center">What people say</h2><div class="reviews">{cards}</div></div></section>'


def video_block(root, vid=VIDEO_ID, caption="The Astonify Show by Dean Carnegie"):
    return f"""<div class="video">
      <div class="video-frame"><iframe src="https://www.youtube.com/embed/{vid}" title="{caption}" loading="lazy"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>
      <span class="video-cap">{caption}</span>
    </div>"""


def cta(root, text="Bring Astonify to your venue, museum or private evening."):
    return f"""<section class="cta"><div class="wrap center">
  <p class="cta-line">{text}</p>
  <a class="btn" href="{root}book/">Ask about a date</a>
  <p class="small">Or call <a href="{PHONE_LINK}">{PHONE}</a></p>
</div></section>"""


# ---------------------------------------------------------------- pages

HOME = f"""
<section class="hero"><div class="wrap hero-in">
  <div class="hero-text">
    <h1>An evening of Victorian parlor magic and a theatrical seance</h1>
    <p class="lead">Prepare for a night of mystifying illusions and wild feats of thought reading, followed by a
    theatrical seance. ASTONIFY transports you to an era when magic and mystery were intertwined with the supernatural,
    and you might even become part of the show.</p>
    <p>It is the perfect blend of conjuring, clairvoyance and ghostly mysteries, performed close up and in period dress,
    just for adults. An evening where mysteries abound, confound, and astound!</p>
    <div class="btns"><a class="btn" href="book/">Bring the show to your venue</a>
    <a class="btn ghost" href="the-show/">About the show</a></div>
  </div>
  <div class="hero-photo">
    <img src="img/spirits-hero.jpg" alt="Dean Carnegie surrounded by the spirits of the past. Astonify, Where Mysteries Abound" width="1025" height="1400">
  </div>
</div></section>

<section class="facts"><div class="wrap facts-in">
  <div><strong>About fifty guests</strong><span>Built for a room, not a theatre</span></div>
  <div><strong>Ages 16 and up</strong><span>A sophisticated evening for adults</span></div>
  <div><strong>Slightly spooky</strong><span>The seance is still part of the show</span></div>
</div></section>

<section class="band"><div class="wrap split">
  <div>
    <h2>Part of the show, if you want to be</h2>
    <p>Not everyone wants to be in the spotlight, and that is fine. Some mysteries happen with the whole room at once.
    Others need a guest or two to step forward. Either way, you will be closer to the magic than you have ever been.</p>
    <p>Stage magic, sleight of hand, mental mysteries and grand illusion, woven through true stories from the
    nineteenth century, when parlor magic and the seance were the most fashionable entertainments of the age.</p>
    <p><a href="the-show/">Read more about the show &rarr;</a></p>
  </div>
  <div>{video_block("")}</div>
</div></section>

{reviews_block()}

<section class="band dark"><div class="wrap split">
  <div><img class="poster" src="img/ghosts-poster.jpg" alt="Poster: Astonify, The Ghosts of Christmas Past" width="900" height="1350" loading="lazy"></div>
  <div>
    <p class="kicker">For December</p>
    <h2>Astonify: The Ghosts of Christmas Past</h2>
    <p>A nineteenth century, Dickens inspired magic show. Charles Dickens was an amateur conjurer, and this is the
    kind of evening he might have presented to his own friends and family.</p>
    <p><a class="btn" href="christmas/">The Christmas show</a></p>
  </div>
</div></section>

<section class="band"><div class="wrap narrow">
  <h2 class="center">Where Astonify has played</h2>
  <ul class="venues">
    <li><strong>The Underground Magic Theater</strong>, Sterling, Virginia. Dean Carnegie's own fifty seat theatre,
    which he co-ran and performed in for four years, 2001 to 2005.</li>
    <li><strong>The Secret Parlor Theatre</strong>, Chantilly, Virginia. Hired to bring the show in, then hired again.</li>
    <li><strong>Fauquier History Museum at the Old Jail</strong>, Warrenton, Virginia. Booked twice.</li>
  </ul>
</div></section>
{cta("")}
"""

HOME_REDIRECT = """<script>
// old WordPress links like astonify.com/?page_id=496 land here; send them to the matching new page
(function(){var p=new URLSearchParams(location.search).get('page_id');
var m={'496':'christmas/','571':'privacy/'};if(p&&m[p])location.replace(m[p]);})();
</script>"""

SHOW = f"""
<section class="pagehead"><div class="wrap narrow center">
  <p class="kicker">The Show</p>
  <h1>Parlor magic, a seance, and the room as the stage</h1>
</div></section>
<section class="band"><div class="wrap split">
  <div>
    <p class="lead">The original Astonify Show was a theatrical recreation of a Victorian parlor magic performance,
    combined with a full light spirit seance. Both were popular in the nineteenth century. The combination is rarely seen today.</p>
    <p>The show has grown since then. It is no longer strictly a period piece, but the heart of it is the same: stage
    magic, sleight of hand, mental mysteries and grand illusion, performed close enough to touch, for a small audience
    who become part of the evening.</p>
    <p>Some routines the whole room does together. Others need a guest or two to step forward. Nobody is pushed into
    anything, and everybody ends up closer to the magic than they expected.</p>
    <p>It is a very unusual and pleasant evening of entertainment, with a slightly spooky edge. And yes, the theatrical
    seance is still part of the show.</p>
  </div>
  <div><img class="photo" src="../img/tintype-rope.jpg" alt="Dean Carnegie in Victorian dress, performing with a rope" width="720" height="960"></div>
</div></section>

<section class="band dark"><div class="wrap split">
  <div><img class="photo" src="../img/tintype-table.jpg" alt="Dean Carnegie at a seance table" width="560" height="560" loading="lazy"></div>
  <div>
    <h2>History you can feel</h2>
    <p>Woven through the evening are true stories from the age of the parlor and the seance. Audiences regularly tell
    us they did not expect a history lesson, and came away smarter as well as amazed.</p>
    <h2>Not a show for children</h2>
    <p>Astonify is designed for ages sixteen and up. It is a sophisticated evening of marvels and mysteries for
    adult minded people. (In December there is a family version, <a href="../christmas/">The Ghosts of Christmas Past</a>.)</p>
  </div>
</div></section>

<section class="band"><div class="wrap narrow">
  <h2 class="center">Where it works best</h2>
  <p>Astonify is built for a room rather than a theatre: about fifty guests, close enough to see everything. It has
  played a purpose built parlor theatre, a history museum housed in an old county jail, and a fifty seat theatre
  Dean Carnegie ran himself. Historic houses and museums, private clubs and private homes, and intimate performance
  spaces all suit it.</p>
  <p>Venues and hosts hire the show for the evening. Tell us the date, the room and roughly how many guests,
  and we will take it from there.</p>
  <div class="center">{video_block("../", SHOW_VIDEO_ID, "The Astonify Show: an interview on Victorian magic and the seance")}</div>
</div></section>
<section class="band dark"><div class="wrap narrow">
  <h2 class="center">Questions people ask</h2>
    <details class="faq"><summary>What is The Astonify Show?</summary><p>An immersive evening of Victorian parlor magic and thought reading, followed by a theatrical seance. It is created and performed by Dean Carnegie, a Nashville, Tennessee illusionist and magic historian, for an intimate room of about fifty guests.</p></details>
    <details class="faq"><summary>Who is it for?</summary><p>Adults. Astonify is designed for ages sixteen and up. In December there is a family friendly version, The Ghosts of Christmas Past.</p></details>
    <details class="faq"><summary>Will I have to go on stage?</summary><p>Only if you want to. Some mysteries involve the whole room at once, and others need a guest or two to step forward. Nobody is pushed into anything.</p></details>
    <details class="faq"><summary>Is the seance real?</summary><p>It is a theatrical seance, performed in the style of the nineteenth century parlor and presented as entertainment. It is slightly spooky, and it is part of the Astonify evening.</p></details>
    <details class="faq"><summary>Is Astonify only in October?</summary><p>No. The show is available all year, and different versions are offered through the year, including The Ghosts of Christmas Past in December.</p></details>
    <details class="faq"><summary>Where is it performed?</summary><p>Astonify is based in Nashville, Tennessee, and is available to travel. Venues, museums, historic sites, clubs and private hosts hire the show for an evening in their own room.</p></details>
    <details class="faq"><summary>How do I book it?</summary><p>Use the form on the Book the Show page, or call 703-404-8902. Tell us the date, the room and roughly how many guests.</p></details>
</div></section>
{cta("../")}
"""

CHRISTMAS = f"""
<section class="pagehead"><div class="wrap narrow center">
  <p class="kicker">For December</p>
  <h1>Astonify: The Ghosts of Christmas Past</h1>
  <p class="lead">A Dickens of a magic show.</p>
</div></section>
<section class="band"><div class="wrap split">
  <div><img class="poster" src="../img/ghosts-poster.jpg" alt="Poster: Carnegie Magic presents Astonify, The Ghosts of Christmas Past, a 19th century Dickens inspired magic show" width="900" height="1350"></div>
  <div>
    <p>Did you know that Charles Dickens, the author of <em>A Tale of Two Cities</em>, <em>Oliver Twist</em> and
    <em>A Christmas Carol</em>, was also an amateur conjurer? Besides being one of the most beloved writers of all time,
    he performed magic for his family and friends, and he was good at it.</p>
    <p>This holiday version of Astonify is a magic show much like the one Mr. Dickens himself might have presented
    in his own parlor. It is presented in the style of a nineteenth century magic show, in Victorian dress, with
    interactive magic, true stories and highly visual surprises. Much of the magic of that era has not been performed
    in well over a century.</p>
    <p>And unlike the regular Astonify evening, this one is <strong>family friendly</strong>. There are moments that spotlight
    children, and moments for the adults too. Who knows, one of them may even have a word with the ghost of old Scrooge himself.</p>
    <h2>A smaller holiday show</h2>
    <p>The Ghosts of Christmas Past is made for intimate rooms: historic houses, museums, libraries, clubs and private
    holiday parties. If you are planning a large company party or a ballroom event, Dean Carnegie has a different
    holiday show for that, and we would be glad to talk it through.</p>
    <p><a class="btn" href="../book/">Ask about a December date</a></p>
  </div>
</div></section>
{cta("../", "Planning a December event? Ask about your date.")}
"""

ABOUT = f"""
<section class="pagehead"><div class="wrap narrow center">
  <p class="kicker">About Carnegie</p>
  <h1>Dean Carnegie, The Artist of Mystery</h1>
</div></section>
<section class="band"><div class="wrap split">
  <div><img class="photo" src="../img/portrait.jpg" alt="Tintype style portrait of Dean Carnegie" width="576" height="433"></div>
  <div>
    <p class="lead">You might think of Carnegie as a genuine traveler through time. Born in the twentieth century,
    he spends most of his time in the nineteenth, but in order to bring the Astonify Show to you, he must journey
    to the twenty first.</p>
    <p>Dean Carnegie is a full time illusionist, escape artist and creator of theatrical mysteries, based in
    Nashville, Tennessee. In thirty years as a working performer he has given more than eight thousand shows.</p>
  </div>
</div></section>
<section class="band dark"><div class="wrap narrow">
  <h2>A few of the rooms he has played</h2>
  <ul class="creds">
    <li>Performed for three U.S. Presidents.</li>
    <li>Two evening performances at The National Theatre in Washington D.C., in the theatre's
    &ldquo;Monday Night at the National&rdquo; series.</li>
    <li>Spoke on the TEDx stage: <em>A Magician's Best Trick: Reality</em>.</li>
    <li>Hosted a French television documentary on Houdini for Arte.</li>
    <li>Ran his own fifty seat venue, The Underground Magic Theater, for four years.</li>
    <li>The Old Warrenton Jail, Warrenton, Virginia, on two separate occasions.</li>
  </ul>
</div></section>
<section class="band"><div class="wrap narrow">
  <h2>The Magic Detective</h2>
  <p>Alongside performing, Carnegie is a historian of magic and show business. He presents lectures on the
  conjurers of the past (or, as he calls them, his friends), writes <a href="https://themagicdetective.com/">The Magic Detective</a>,
  with more than seven hundred articles on magic history since 2011, and hosts the
  <a href="https://magicdetectivepodcast.com/">Magic Detective Podcast</a>.</p>
  <h2>The painter</h2>
  <p>He is also a painter, and his usual subject is the magicians of the past. His magic artwork has appeared on the
  cover of Elan Magazine and twice on the cover of MAGIC Magazine. See the paintings at
  <a href="https://art.carnegiemagic.com/">art.carnegiemagic.com</a>.</p>
  <p>For everything else, including his larger stage shows, visit <a href="https://carnegiemagic.com/">CarnegieMagic.com</a>.</p>
</div></section>
{cta("../")}
"""

BOOK = f"""
<section class="pagehead"><div class="wrap narrow center">
  <p class="kicker">Book the Show</p>
  <h1>Bring Astonify to your room</h1>
  <p class="lead">Tell us the date you have in mind, where the show would be, and roughly how many guests.
  We will come back to you with availability and details.</p>
</div></section>
<section class="band"><div class="wrap narrow">
  <div class="contact-row">
    <div><strong>Call</strong><a href="{PHONE_LINK}">{PHONE}</a></div>
    <div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
  <p class="center">Press enquiries are welcome at the same address.</p>
  <div class="form-box">
    <script src="https://mago.co/Scripts/form.js"></script>
    <script>
      var magoForm = new MagoForm();
      magoForm.initialize({{'formId':'{MAGO_FORM_ID}','autoResize':true,'ssl':true}});
      magoForm.display();
    </script>
    <noscript><p>The booking form needs JavaScript. Please call or email instead.</p></noscript>
  </div>
</div></section>
"""

PRIVACY = f"""
<section class="pagehead"><div class="wrap narrow center"><h1>Privacy</h1></div></section>
<section class="band"><div class="wrap narrow">
  <p>This website is run by Carnegie Magic. It does not use advertising trackers and does not sell or share
  your information.</p>
  <p>If you send an enquiry through the booking form, the details you type in (such as your name, email address,
  phone number and event details) are delivered to us by our booking form provider so that we can reply to you.
  We use them only to answer your enquiry and arrange your event.</p>
  <p>Videos on this site are played by YouTube, which has its own privacy policy.</p>
  <p>To ask what we hold about you, or to have it deleted, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>
"""

NOT_FOUND = """
<section class="pagehead"><div class="wrap narrow center">
  <h1>This page has vanished</h1>
  <p class="lead">A fine trick, but not the one we intended.</p>
  <p><a class="btn" href="/">Back to the Astonify home page</a></p>
</div></section>
"""

PAGES = [
    ("", "The Astonify Show | Victorian Magic and Seance Show, Nashville | Dean Carnegie",
     "Astonify is an immersive Victorian magic and theatrical seance show by Nashville illusionist Dean Carnegie, for an intimate room of about fifty adults. Book it for your venue, museum or private event.",
     HOME, SCHEMA, HOME_REDIRECT),
    ("the-show/", "The Show: Parlor Magic and a Theatrical Seance | Astonify, Nashville",
     "Stage magic, sleight of hand, mental mysteries and grand illusion, with a theatrical seance, performed close up for about fifty guests aged 16 and up.",
     SHOW, FAQ_SCHEMA, ""),
    ("christmas/", "The Ghosts of Christmas Past | Dickens Christmas Magic Show, Nashville | Astonify",
     "Astonify: The Ghosts of Christmas Past, a family friendly, Dickens inspired nineteenth century magic show for intimate December events.",
     CHRISTMAS, "", ""),
    ("about/", "About Dean Carnegie, Nashville Illusionist | The Astonify Show",
     "Dean Carnegie, The Artist of Mystery: Nashville illusionist, magic historian and painter. Thirty years, more than eight thousand shows.",
     ABOUT, "", ""),
    ("book/", "Book the Show | The Astonify Show, Nashville",
     "Bring The Astonify Show to your venue, museum, club or private evening. Ask about availability.",
     BOOK, "", ""),
    ("privacy/", "Privacy | The Astonify Show", "Privacy information for astonify.com.", PRIVACY, "", ""),
]


# llms.txt: a plain summary for AI assistants (the emerging llmstxt.org convention)
LLMS = f"""# The Astonify Show

> An immersive evening of Victorian parlor magic, thought reading and a theatrical seance, created and performed
> by Dean Carnegie, a Nashville, Tennessee illusionist and magic historian. Built for an intimate room of about
> fifty guests, ages 16 and up. Available all year to venues, museums, historic sites, clubs and private hosts.

- Performer: Dean Carnegie, "The Artist of Mystery". Thirty years as a full time performer, more than eight thousand
  shows, performed for three U.S. Presidents, two evening performances at The National Theatre in Washington D.C.,
  a TEDx speaker, host of a French television documentary on Houdini for Arte. Writes The Magic Detective and hosts
  the Magic Detective Podcast.
- Venues: The Underground Magic Theater (his own fifty seat theatre, Sterling, Virginia, 2001 to 2005), The Secret
  Parlor Theatre (Chantilly, Virginia), Fauquier History Museum at the Old Jail (Warrenton, Virginia, twice).
- December version: Astonify: The Ghosts of Christmas Past, a family friendly, Dickens inspired nineteenth century
  magic show for intimate holiday events.
- Booking: {SITE}book/ or {PHONE}, {EMAIL}

## Pages
- [Home]({SITE}): what the evening is, reviews, where it has played
- [The Show]({SITE}the-show/): the show in detail, with common questions answered
- [The Ghosts of Christmas Past]({SITE}christmas/): the December, family friendly version
- [About Dean Carnegie]({SITE}about/): the performer
- [Book the Show]({SITE}book/): enquiry form, phone and email
"""


def write(path, text):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def redirect(target):
    url = SITE + target
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title>
<link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0; url={url}"></head>
<body><p>This page has moved to <a href="{url}">{url}</a>.</p></body></html>
"""


def main():
    for slug, title, desc, body, head, end in PAGES:
        write(slug + "index.html", page(slug, title, desc, body, head, end))
    write("404.html", page("404/", "Page not found | The Astonify Show", "Page not found.", NOT_FOUND)
          .replace('href="../', 'href="/').replace('src="../', 'src="/'))
    for old, new in OLD_PAGES.items():
        write(old + "index.html", redirect(new))
    bots = ["Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
            "PerplexityBot", "Google-Extended", "Applebot", "Applebot-Extended"]
    write("robots.txt", "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
          + f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    write("llms.txt", LLMS)
    urls = "".join(f"<url><loc>{SITE}{s}</loc><lastmod>{datetime.date.today()}</lastmod></url>" for s, *_ in PAGES if s != "privacy/")
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("CNAME", "astonify.com\n")
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
