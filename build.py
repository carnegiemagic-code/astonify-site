#!/usr/bin/env python3
"""Builds astonify.com. Edit the text below, run `python3 build.py`, then push.

Rebuilt Oct 2026 from the last good copy of the old WordPress site (Internet Archive, Sept 2022),
updated to how the show is sold now: venues and private hosts hire it, in person (no more Zoom).
Rules for copy here: no em dashes, no prices, never describe how a routine works.
"""
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
 "@type": "TheaterEvent",
 "name": "The Astonify Show",
 "description": "An immersive evening of Victorian parlor magic and a theatrical seance, performed by Dean Carnegie for an intimate room of about fifty guests.",
 "url": "https://astonify.com/",
 "image": "https://astonify.com/img/og.jpg",
 "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
 "eventStatus": "https://schema.org/EventScheduled",
 "typicalAgeRange": "16-",
 "performer": {"@type": "Person", "name": "Dean Carnegie", "url": "https://carnegiemagic.com/"},
 "organizer": {"@type": "Organization", "name": "Carnegie Magic", "url": "https://carnegiemagic.com/", "telephone": "+1-703-404-8902", "email": "info@carnegiemagic.com"}
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

VIDEO_ID = "iogvFyMVQO0"  # The Astonify Show, filmed from the audience at The Secret Parlor Theatre


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


def video_block(root):
    return f"""<a class="video" href="https://www.youtube.com/watch?v={VIDEO_ID}" target="_blank" rel="noopener">
      <img src="https://i.ytimg.com/vi/{VIDEO_ID}/hqdefault.jpg" alt="Watch a clip of The Astonify Show" loading="lazy" width="480" height="360">
      <span class="play" aria-hidden="true"></span>
      <span class="video-cap">Watch a clip, filmed from the audience at The Secret Parlor Theatre</span>
    </a>"""


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
    <p class="lead">ASTONIFY is a live, immersive magic show. The audience becomes part of the evening, sometimes from
    their seats and sometimes in the middle of the mystery itself. There is no stage to hide behind. The whole room is the stage.</p>
    <p>You will see impossible things up close, from the side, and from angles a theatre never allows.
    Imagine watching a person cut in half only a few feet from your chair.</p>
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
  <div class="center">{video_block("../")}</div>
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
  <p>Video links on this site go to YouTube, which has its own privacy policy.</p>
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
    ("", "The Astonify Show | Victorian Parlor Magic and a Seance with Dean Carnegie",
     "Astonify is an immersive evening of Victorian parlor magic and a theatrical seance with Dean Carnegie, for an intimate room of about fifty adults. Book it for your venue or private event.",
     HOME, SCHEMA, HOME_REDIRECT),
    ("the-show/", "The Show | The Astonify Show",
     "Stage magic, sleight of hand, mental mysteries and grand illusion, with a theatrical seance, performed close up for about fifty guests aged 16 and up.",
     SHOW, "", ""),
    ("christmas/", "The Ghosts of Christmas Past | A Dickens Magic Show | Astonify",
     "Astonify: The Ghosts of Christmas Past, a family friendly, Dickens inspired nineteenth century magic show for intimate December events.",
     CHRISTMAS, "", ""),
    ("about/", "About Dean Carnegie | The Astonify Show",
     "Dean Carnegie, The Artist of Mystery: Nashville illusionist, magic historian and painter. Thirty years, more than eight thousand shows.",
     ABOUT, "", ""),
    ("book/", "Book the Show | The Astonify Show",
     "Bring The Astonify Show to your venue, museum, club or private evening. Ask about availability.",
     BOOK, "", ""),
    ("privacy/", "Privacy | The Astonify Show", "Privacy information for astonify.com.", PRIVACY, "", ""),
]


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
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{s}</loc></url>" for s, *_ in PAGES if s != "privacy/")
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("CNAME", "astonify.com\n")
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
